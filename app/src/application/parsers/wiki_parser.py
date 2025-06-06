import asyncio
from concurrent.futures import ThreadPoolExecutor

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from src.application.errors import NewSiteStructureError
from src.domain.article import Article
from src.domain.base_url_parser import BaseUrlParser


# we also could add some kind of set to store previously parsed links not do it again
class WikiParser(BaseUrlParser):
    MAIN_BLOCK_ID = 'mw-content-text'
    DOMAIN = 'wikipedia.org'

    def __init__(self, aiohttp_session: ClientSession, thread_pool: ThreadPoolExecutor, nesting: int = 5) -> None:
        self.session = aiohttp_session
        self.thread_pool = thread_pool
        self.nesting = nesting

    async def parse_url(self, url: str) -> Article:
        async with self.session.get(url) as response:
            print(response.status)
            text = await response.text()

        parsed_text, parsed_urls = asyncio.get_running_loop().run_in_executor(
            self.thread_pool,
            self.parse_html,
            url,
            text,
        )
        article = Article(parsed_text)

        parsed_articles = await self.parse_siblings(parsed_urls)
        article.siblings = parsed_articles

        return article

    def parse_html(self, url: str, text: str) -> tuple[str, list[str]]:
        soup = BeautifulSoup(text)
        main_block = soup.find(id=self.MAIN_BLOCK_ID)
        if main_block is None:
            msg = 'main block not found in wiki page'
            raise NewSiteStructureError(msg)

        parsed_text = main_block.get_text()

        urls = main_block.find_all('a')
        cleaned_urls = self.find_siblings(url, urls)

        return parsed_text, cleaned_urls

    def find_siblings(self, main_url: str, urls: list[str]) -> list[str]:
        sibling_urls: list[str] = []
        for url in urls:
            # check if it is same page
            if url.startswith(main_url):
                continue

            # check if it is not wiki page
            domain_end_index: int = url.find('/', 8)
            if url[:domain_end_index].endswith(self.DOMAIN):
                sibling_urls.append(url)

        return sibling_urls

    async def parse_siblings(self, parsed_urls: list[str]) -> list[Article]:
        return (
            [
                await WikiParser(self.session, self.thread_pool, self.nesting - 1).parse_url(parsed_url)
                for parsed_url in parsed_urls
            ]
            if self.nesting > 0
            else []
        )

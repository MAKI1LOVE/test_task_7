import asyncio
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, replace
from typing import Any
from urllib.parse import urljoin

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from src.domain.article import Article
from src.domain.base_url_parser import BaseUrlParser


@dataclass
class ParserSettings:
    NESTING: int


# we also could add some kind of set to store previously parsed links not do it again
class WikiParser(BaseUrlParser):
    MAIN_BLOCK_ID = 'mw-content-text'
    MAIN_DOMAIN = 'wikipedia.org'

    def __init__(
        self,
        aiohttp_session: ClientSession,
        thread_pool: ThreadPoolExecutor,
        parser_settings: ParserSettings,
    ) -> None:
        self.session = aiohttp_session
        self.thread_pool = thread_pool
        self.parser_settings = parser_settings

    async def parse(self, url: str) -> Article | None:
        self.url = url
        self.parsed_articles: dict[str, Article] = {}

        return await self.parse_url(self.url, self.parser_settings.NESTING)

    async def parse_url(self, url: str, nesting: int) -> Article | None:
        async with self.session.get(url) as response:
            if response.status != 200 or 'text/html' not in response.content_type:
                return None
            text = await response.text()

        parsed_text, parsed_urls = await asyncio.get_running_loop().run_in_executor(
            self.thread_pool,
            self.parse_html,
            text,
        )
        if parsed_text is None:
            return None

        if url not in self.parsed_articles:
            article = Article(url=url, parsed_text=parsed_text)
            self.parsed_articles[url] = article
        else:
            article = self.parsed_articles[url]

        if nesting > 0:
             article.siblings = await self.parse_siblings(article.url, parsed_urls, nesting - 1)

        return article

    def parse_html(self, text: str) -> tuple[str | None, list[str]]:
        soup = BeautifulSoup(text, 'lxml')
        main_block = soup.find(id=self.MAIN_BLOCK_ID)
        if main_block is None:
            return None, []

        parsed_text = main_block.get_text()

        urls = main_block.find_all('a')
        cleaned_urls = self.find_siblings(urls)

        return parsed_text, cleaned_urls

    def find_siblings(self, urls: list[Any]) -> list[str]:
        sibling_urls: set[str] = set()
        for url_block in urls:
            # check if it is same page
            url = url_block.get('href')
            # some anchors may not contain href
            if url is None:
                continue

            if url.startswith((self.url, '#')):
                continue

            # check if it is not wiki page
            domain_end_index: int = url.find('/', 8)
            if url.startswith('/') or url[:domain_end_index].endswith(self.MAIN_DOMAIN):
                sibling_urls.add(url)

        return list(sibling_urls)

    async def parse_siblings(self, main_url: str, parsed_urls: list[str], nesting: int) -> list[Article]:
        tasks = [
            self.parse_url(urljoin(main_url, parsed_url), nesting)
            for parsed_url in parsed_urls
        ]
        articles = await asyncio.gather(*tasks)

        return [article for article in articles if article is not None]

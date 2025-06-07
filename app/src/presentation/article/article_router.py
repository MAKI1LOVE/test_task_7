from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.domain.base_parser_service import BaseParserService

router = APIRouter(prefix='/articles', tags=['articles'], route_class=DishkaRoute)


@router.get('/search')
async def start_searching_articles(
    url: str,
    parser_service: FromDishka[BaseParserService],
) -> dict[str, str]:
    await parser_service.parse(url)
    return {'status': 'ok'}

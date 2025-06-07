from fastapi import APIRouter

from src.presentation.article.article_router import router as article_router

router = APIRouter(prefix='')
router.include_router(article_router)

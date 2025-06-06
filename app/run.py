import uvicorn

from src.main import app_factory

if __name__ == '__main__':
    uvicorn.run(app_factory(), factory=True)

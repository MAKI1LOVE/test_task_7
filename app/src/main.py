from fastapi import FastAPI


def app_factory() -> FastAPI:
    app = create_app()
    

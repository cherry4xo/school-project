from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from tortoise.contrib.fastapi import register_tortoise

from src.app import router
from src.config import config


app = FastAPI(
    title="BMSTU project API",
    description='Author - Kulakov Nikita (AKA cherry4xo)',
    version='0.1.0'
)

app.include_router(router.api_router)

register_tortoise(
    app,
    db_url=f'mysql://{config.MYSQL_NAME}:{config.MYSQL_PASS}@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DB_NAME}',
    modules={'models': config.MODELS},
    generate_schemas=True,
    add_exception_handlers=True
)
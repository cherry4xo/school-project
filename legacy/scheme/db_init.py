import models_fixed
from config import MYSQL_NAME, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB_NAME
from tortoise import Tortoise, run_async

async def init():
    await Tortoise.init(db_url=f"mysql://{MYSQL_NAME}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB_NAME}", 
                        modules={"models": ["models_fixed"]})
    await Tortoise.generate_schemas()

if __name__ == "__main__":
    run_async(init())
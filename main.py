import models
from config import USER_NAME, USER_PASS, DB_IP, DB_PORT, DB_NAME
from tortoise import Tortoise, run_async

async def init():
    await Tortoise.init(db_url=f"mysql://{USER_NAME}:{USER_PASS}@{DB_IP}:{DB_PORT}/{DB_NAME}", 
                        modules={"models": ["models"]})
    await Tortoise.generate_schemas()

if __name__ == "__main__":
    run_async(init())
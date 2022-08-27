from  fastapi import FastAPI
from config import setting
from database import engine
from models import Base
from routers import users, items, login
from webapps.routers import item as web_item
from webapps.routers import users as web_users
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

tags_metadata = [

        {
            "name": "user",
            "description": "this is user route"
            },
        {
            "name": "items",
            "description": "this is product route"
            }

        ]

app = FastAPI(
        title=setting.TITLE,
        version = setting.VERSION,
        description=setting.DESCRIPTION,
       openapi_tags=tags_metadata,
        contact = {
            "name":setting.NAME,
            "email": setting.EMAIL
            }
        )

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(items.router)
app.include_router(login.router)
app.include_router(web_item.router)
app.include_router(web_users.router)


from  fastapi import FastAPI
from config import setting
from database import engine
from models import Base
from routers import users, items, login

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

app.include_router(users.router)
app.include_router(items.router)
app.include_router(login.router)



from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import Items

router = APIRouter(include_in_schema = False)

templates = Jinja2Templates(directory="templates")

@router.get("/")
def home(request: Request, db:Session=Depends(get_db)):
    items = db.query(Items).all()
    return  templates.TemplateResponse("item_homepage.html", {"request": request, "items": items})

@router.get("/detail/{id}")
def item_details(request:Request, id:int, db:Session=Depends(get_db)):
    item = db.query(Items).filter(Items.id==id).first()
    return templates.TemplateResponse("item_details.html", {"request":request, "item":item})














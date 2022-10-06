from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import Items, User
from jose import jwt
from config import setting
from datetime import datetime
from typing import Optional

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="templates")


@router.get("/")
def home(request: Request, db: Session = Depends(get_db), msg: str = None):
    items = db.query(Items).all()
    return templates.TemplateResponse(
        "item_homepage.html", {"request": request, "items": items, "msg": msg}
    )


@router.get("/detail/{id}")
def item_details(request: Request, id: int, db: Session = Depends(get_db)):
    item = db.query(Items).filter(Items.id == id).first()
    user = db.query(User).filter(User.id == item.owner_id).first()
    return templates.TemplateResponse(
        "item_details.html", {"request": request, "item": item, "user": user}
    )


@router.get("/create-an-item")
def create_item(request: Request, msg: str = None):
    return templates.TemplateResponse(
        "create_item.html", {"request": request, "msg": msg}
    )


@router.post("/create-an-item")
async def create_item(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    title = form.get("title")
    description = form.get("description")
    errors = []
    if not title or len(title) < 4:
        errors.append("Sorry the title should be greater than 4 characters!!")
    if not description or len(description) < 10:
        errors.append("Please give more descriptions")
    if len(errors) > 0:
        return templates.TemplateResponse(
            "create_item.html", {"request": request, "errors": errors}
        )
    try:
        token = request.cookies.get("access_token")
        if token is None:
            errors.append("Kindly login first")
            return templates.TemplateResponse(
                "create_item.html", {"request": request, "errors": errors}
            )
        else:
            scheme, _, param = token.partition(" ")
            payload = jwt.decode(
                param, setting.SECRET_KEY, algorithms=setting.ALGORITHM
            )
            email = payload.get("sub")
            user = db.query(User).filter(User.email == email).first()
            if user is None:
                errors.append(
                    "You are not authenticated please create an account or login first you if have one"
                )
                return templates.TemplateResponse(
                    "create_item.html", {"request": request, "errors": errors}
                )
            else:
                item = Items(
                    title=title,
                    description=description,
                    date_posted=datetime.now().date(),
                    owner_id=user.id,
                )
                db.add(item)
                db.commit()
                db.refresh(item)
                return responses.RedirectResponse(
                    f"/detail/{item.id}", status_code=status.HTTP_302_FOUND
                )
    except Exception as e:
        errors.append("something went wrong")
        return templates.TemplateResponse(
            "create_item.html", {"request": request, "errors": errors}
        )


@router.get("/delete-an-item")
def item_to_delete(request: Request, db: Session = Depends(get_db)):
    errors = []
    token = request.cookies.get("access_token")
    if token is None:
        errors.append("You are not logged in")
        return templates.TemplateResponse(
            "item_to_delete.html", {"request": request, "errors": errors}
        )
    else:
        try:
            scheme, _, param = token.partition(" ")
            payload = jwt.decode(
                param, setting.SECRET_KEY, algorithms=setting.ALGORITHM
            )
            email = payload.get("sub")
            user = db.query(User).filter(User.email == email).first()
            items = db.query(Items).filter(Items.owner_id == user.id).all()
            return templates.TemplateResponse(
                "item_to_delete.html", {"request": request, "items": items}
            )
        except Exception as e:
            errors.append("something is wrong")
            print(e)
            return templates.TemplateResponse(
                "item_to_delete.html", {"request": request, "errors": errors}
            )

@router.get("/search")
def search(request: Request, query:Optional[str], db:Session=Depends(get_db)):
    items = db.query(Items).filter(Items.title.contains(query)).all()
    return templates.TemplateResponse("item_homepage.html", {"request": request, "items": items})
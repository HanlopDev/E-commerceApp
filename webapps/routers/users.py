from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from hashing import Hasher
from sqlalchemy.orm import Session
from database import get_db
from models import User
from sqlalchemy.exc import IntegrityError

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/register")
def registration(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def registration(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    errors = []
    if len(password) < 6:
        errors.append("password too short")
        return templates.TemplateResponse(
            "register.html", {"request": request, "errors": errors}
        )
    user = User(email=email, password=Hasher.get_hash_password(password))
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return responses.RedirectResponse(
            "/login?msg=successfully registered", status_code=status.HTTP_302_FOUND
        )
    except IntegrityError:
        errors.append("user already exist")
        return templates.TemplateResponse(
            "register.html", {"request": request, "errors": errors}
        )

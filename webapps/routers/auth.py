from fastapi import APIRouter, Request, Depends, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import User
from hashing import Hasher
from config import setting
from jose import jwt

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")

@router.get("/login")
def login(request:Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request:Request,response:Response,  db:Session=Depends(get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    errors = []
    if not email:
        errors.append("Please enter valid email")
    if not password or len(password) < 6:
        errors.append("Password needs to be more than six characters")
    try:
        user = db.query(User).filter(User.email==email).first()
        if user is None:
            errors.append("User does'nt exist")
            return templates.TemplateResponse("login.html", {"request":request, "errors":errors})
        else:
            if Hasher.verify_password(password, user.password): 
                data = {"sub":email}
                jwt_token = jwt.encode(data, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
                msg = "Login successfully"
                response = templates.TemplateResponse("login.html", {"request":request, "msg":msg})
                response.set_cookie(key="access_token", value=f"Bearer {jwt_token}", httponly=True)
                return response
            else:
                errors.append("Invalid password")
                return templates.TemplateResponse("login.html", {"request":request, "errors":errors})
    except:
        errors.append("something wrong!!")
        return templates.TemplateResponse("login.html", {"request":request, "errors":errors})

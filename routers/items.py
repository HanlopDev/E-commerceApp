from fastapi import APIRouter, Depends, HTTPException, status   
from schemas import ItemCreate, ShowItem
from models import Items, User
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from routers.login import oauth2_scheme
from jose import jwt
from config import setting

router = APIRouter()


def get_user_from_token(db, token):
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="unable to verify credential",
            )
        user = db.query(User).filter(User.email == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="unable to verify credential",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="unable to verify credential",
        )
    return user


@router.get("/item/all", tags=["items"], response_model=List[ShowItem])
def retrieve_al_items(db: Session = Depends(get_db)):
    items = db.query(Items).all()
    return items

@router.get("/item/autocomplete")    
def autocomplete(term: Optional[str], db:Session=Depends(get_db)):
    items = db.query(Items).filter(Items.title.contains(term)).all()
    sugestions = []
    for item in items:
        sugestions.append(item.title)
        return sugestions
        
@router.get("/item/{id}", tags=["items"], response_model=ShowItem)
def get_item_by_id(id: int, db: Session = Depends(get_db)):
    item = db.query(Items).filter(Items.id == id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {id} does'nt exist"
        )
    return item


@router.put("/item/update/{id}", tags=["items"])
def update_item_by_id(
    id: int,
    item: ItemCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    user = get_user_from_token(db, token)
    existing_item = db.query(Items).filter(Items.id == id)
    if not existing_item.first():
        return {"message": f"no details exist for Item ID {id}"}
    if existing_item.first().owner_id == user.id:
        existing_item.update(jsonable_encoder(item))
        db.commit()
        return {"message": f"Detail for item ID {id} successsfully updated"}
    else:
        return {"meassage": {"you are not authorized"}}


@router.delete("/item/delete/{id}", tags=["items"])
def delete_item_by_id(
    id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    user = get_user_from_token(db, token)
    existing_item = db.query(Items).filter(Items.id == id)
    if not existing_item.first():
        return {"message" f"No detail exist for item ID {id}"}
    if existing_item.first().owner_id == user.id:
        existing_item.delete()
        db.commit()
        return {"message": f"Item with ID {id} is deleted"}
    else:
        return {"message": "you are not authorized"}



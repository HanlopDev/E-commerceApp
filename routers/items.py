from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ItemCreate, ShowItem
from models import Items
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from fastapi.encoders import jsonable_encoder
from routers.login import oauth2_scheme

router = APIRouter()

@router.post("/items", tags=["items"], response_model=ShowItem)
def create_item(item: ItemCreate, db: Session=Depends(get_db), token:str=Depends(oauth2_scheme)):
    date_posted = datetime.now().date()
    owner_id = 1
    item = Items(**item.dict(), date_posted = date_posted, owner_id = owner_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/item/all", tags=["items"], response_model=List[ShowItem])
def retrieve_al_items(db: Session=Depends(get_db)):
    items = db.query(Items).all()
    return items

@router.get("/item/{id}", tags=["items"], response_model=ShowItem)
def get_item_by_id(id: int, db: Session=Depends(get_db)):
    item = db.query(Items).filter(Items.id==id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {id} does'nt exist")
    return item

@router.put("/update/{id}", tags=["items"])
def update_item_by_id(id: int, item: ItemCreate, db: Session=Depends(get_db), token:str=Depends(oauth2_scheme)):
    existing_item = db.query(Items).filter(Items.id==id)
    if not existing_item.first():
        return {"message": f"no details exist for Item ID {id}"}
    existing_item.update(jsonable_encoder(item))
    db.commit()
    return {"message": f"Detail for item ID {id} successsfully updated"}

@router.delete("/item/delete/{id}", tags=["items"])
def delete_item_by_id(id:int, db: Session=Depends(get_db), token:str=Depends(oauth2_scheme)):
    existing_item = db.query(Items).filter(Items.id==id)
    if not existing_item.first():
        return {"message" f"No detail exist for item ID {id}"}
    existing_item.delete()
    db.commit()
    return {"message": f"Item with ID {id} is deleted"}    

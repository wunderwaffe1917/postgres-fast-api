from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_active_user
from app.db.session import get_db
from app.models.item import Item
from app.models.user import User
from app.schemas.item import Item as ItemSchema, ItemCreate, ItemUpdate

router = APIRouter()

@router.get("/", response_model=List[ItemSchema])
def read_items(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve items.
    """
    if current_user.is_superuser:
        items = db.query(Item).offset(skip).limit(limit).all()
    else:
        items = db.query(Item).filter(Item.owner_id == current_user.id).offset(skip).limit(limit).all()
    return items

@router.post("/", response_model=ItemSchema)
def create_item(
    *,
    db: Session = Depends(get_db),
    item_in: ItemCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    item = Item(
        title=item_in.title,
        description=item_in.description,
        owner_id=current_user.id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/{item_id}", response_model=ItemSchema)
def read_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return item

@router.put("/{item_id}", response_model=ItemSchema)
def update_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    item_in: ItemUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update an item.
    """
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = item_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}", response_model=ItemSchema)
def delete_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(item)
    db.commit()
    return item
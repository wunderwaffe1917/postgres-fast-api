from typing import Optional
from pydantic import BaseModel, ConfigDict

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class ItemInDBBase(ItemBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)

class Item(ItemInDBBase):
    pass
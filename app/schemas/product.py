from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price_paise: int
    stock: int = 0

class ProductOut(BaseModel):
    id: int
    name: str
    description: str | None
    price_paise: int
    stock: int
    is_active: bool

    class Config:
        from_attributes = True
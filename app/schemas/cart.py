from pydantic import BaseModel

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

class CartOut(BaseModel):
    id: int
    items: list[CartItemOut]

    class Config:
        from_attributes = True
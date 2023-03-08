from pydantic import BaseModel


class ProductData(BaseModel):
    public_id: str
    name: str
    sku: str
    price: float
    brand: str
    queries: int

    class Config():
        orm_mode = True

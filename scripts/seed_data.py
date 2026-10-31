from app.core.database import SessionLocal
from app.models.product import Product

db = SessionLocal()

product = db.query(Product).filter(Product.id == 1).first()
if product:
    product.stock = 500
    product.is_active = True
else:
    product = Product(
        name="Wireless Mouse",
        description="Basic USB wireless mouse",
        price_paise=59900,
        stock=500,
        is_active=True,
    )
    db.add(product)

db.commit()
db.close()
print("Seed complete: product 1 stock topped up.")
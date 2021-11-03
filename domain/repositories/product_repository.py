from domain.db.config import session
from domain.entities.product import Product

def get_all_products() -> list[Product]:
  return session.query(Product).all()

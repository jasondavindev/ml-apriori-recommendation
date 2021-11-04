from domain.db.config import session
from domain.entities.product import Product


def get_all_products() -> list[Product]:
    return session.query(Product).all()


def get_product_by_name(name: str):
    return session.query(Product).filter_by(product_name=name).first()


def create_product(product_name: str):
    product = Product(product_name)
    session.add(product)
    return product

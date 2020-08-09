from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import and_

from Models import Base


class Product(Base.dec_base):
    __tablename__ = 'products'

    product_id = Column(Integer(), primary_key=True)
    product_name = Column(String(25), nullable=False)
    product_type = Column(String(25))
    product_size = Column(String(25))
    selling_price = Column(Float(5, 2), nullable=False)
    actual_price = Column(Float(5, 2))

    def __repr__(self):
        return f'product {self.product_name}'

    @classmethod
    def get_product(cls, product_id):
        return Base.session.query(cls).filter_by(product_id=product_id).first()

    @classmethod
    def get_all_products(cls):
        return Base.session.query(cls).all()

    @classmethod
    def get_product_name_list(cls):
        return Base.session.query(cls.product_name).distinct().all()

    @classmethod
    def get_product_type_list(cls):
        return Base.session.query(cls.product_type).distinct().all()

    @classmethod
    def search_products(cls, product_id=None, product_name="", product_type="", product_size="", selling_price=0):
        if product_id:
            return cls.get_product(product_id)

        if selling_price > 0:
            return Base.session.query(cls).filter(and_(
                Product.product_name.like(f'%{product_name}%'),
                Product.product_type.like(f'%{product_type}%'),
                Product.product_size.like(f'%{product_size}%'),
                Product.selling_price == selling_price
            )).all()

        return Base.session.query(cls).filter(and_(
            Product.product_name.like(f'%{product_name}%'),
            Product.product_type.like(f'%{product_type}%'),
            Product.product_size.like(f'%{product_size}%'),
        )).all()

    @classmethod
    def add_product(cls, product):
        product_name, product_type, product_size, selling_price, actual_price = product

        # if actual_price == 0 or actual_price == '':
        #     actual_price = selling_price

        product = Product(product_name=product_name, product_type=product_type,
                          product_size=product_size, selling_price=selling_price, actual_price=actual_price)
        Base.session.add(product)
        Base.session.commit()

    @classmethod
    def delete_product(cls, product_id):
        product = cls.get_product(product_id)

        if product:
            Base.session.delete(product)
            Base.session.commit()
        else:
            print(f"product_id '{product_id}' not found in db!")

    @classmethod
    def update_product(cls, product):
        product_id, product_name, product_type, product_size, selling_price, actual_price = product

        # if actual_price == 0 or actual_price == '':
        #     actual_price = selling_price

        product = cls.get_product(product_id)

        if product:
            product.product_name = product_name
            product.product_type = product_type
            product.product_size = product_size
            product.selling_price = selling_price
            product.actual_price = actual_price
            Base.session.commit()
        else:
            print(f"product_id '{product_id}' not found in db!")

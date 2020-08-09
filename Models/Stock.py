from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import and_

from Models import Base
from Models.Product import Product


class Stock(Base.dec_base):
    __tablename__ = 'stock'
    product_id = Column(Integer(), ForeignKey('products.product_id'), primary_key=True)
    quantity = Column(Integer(), nullable=False)

    def __repr__(self):
        return f'Stock {self.product_id}'

    @classmethod
    def get_stock(cls, product_id):
        return Base.session.query(cls).filter_by(product_id=product_id).first()

    @classmethod
    def get_all_stocks(cls):
        return Base.session.query(Product, Stock).outerjoin(Stock)\
            .order_by(Product.product_name, Product.product_type).all()

    @classmethod
    def search_stock(cls, product_id=None, product_name="", product_type="", product_size="", selling_price=0):
        if product_id:
            return Base.session.query(Product, Stock).outerjoin(Stock).filter_by(product_id=str(product_id))\
                .order_by(Product.product_name, Product.product_type).all()

        if selling_price > 0:
            return Base.session.query(Product, Stock).outerjoin(Stock).filter(and_(
                Product.product_name.like(f'%{product_name}%'),
                Product.product_type.like(f'%{product_type}%'),
                Product.product_size.like(f'%{product_size}%'),
                Product.selling_price == selling_price
            )).all()

        return Base.session.query(Product, Stock).outerjoin(Stock).filter(and_(
            Product.product_name.like(f'%{product_name}%'),
            Product.product_type.like(f'%{product_type}%'),
            Product.product_size.like(f'%{product_size}%'),
        )).all()

    @staticmethod
    def add_stock(stock):
        product_id, quantity = stock

        stock = Stock(product_id=product_id, quantity=quantity)
        Base.session.add(stock)
        Base.session.commit()

    @classmethod
    def clear_stock(cls, product_id):
        stock = cls.get_stock(product_id)

        if stock:
            print(f"product_id: '{product_id}' available stock: {stock.quantity} in db")
            stock.quantity = 0
            # session.delete(stock)
            Base.session.commit()
        else:
            print(f"product_id: '{product_id}' not found in db!")

    @classmethod
    def compute_stock(cls, stock):
        product_id, quantity = stock

        my_stock = cls.get_stock(product_id)

        if my_stock:
            if (my_stock.quantity - quantity) < 0:
                my_stock.quantity = 0
            else:
                my_stock.quantity = my_stock.quantity - quantity

            Base.session.commit()

    @classmethod
    def update_stock(cls, stock):
        product_id, quantity = stock

        my_stock = cls.get_stock(product_id)

        if my_stock:
            my_stock.quantity = quantity
            Base.session.commit()
        else:
            cls.add_stock(stock)
            # print(f"product_id '{product_id}' not found in db!")

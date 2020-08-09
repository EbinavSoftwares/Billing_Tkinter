from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey

from Models import Base


class Purchase(Base):
    __tablename__ = 'purchase'
    purchase_date = Column(DateTime, default=datetime.now())
    product_id = Column(Integer(), ForeignKey('products.product_id'), primary_key=True)
    quantity = Column(Integer(), nullable=False)

    def __repr__(self):
        return f'purchase {self.product_id}'

    @classmethod
    def get_purchase(cls, purchase_date, product_id):
        return Base.session.query(cls).filter_by(purchase_date=purchase_date, product_id=product_id).first()

    @staticmethod
    def add_purchase(purchase):
        purchase_date, product_id, quantity = purchase

        purchase = Purchase(purchase_date=purchase_date, product_id=product_id, quantity=quantity)
        Base.session.add(purchase)
        Base.session.commit()

    def delete_purchase(self, purchase_date, product_id):
        purchase = self.get_purcahse(purchase_date, product_id)

        if purchase:
            Base.session.delete(purchase)
            Base.session.commit()
        else:
            print(f"purchase '{purchase_date, product_id}' not found in db!")

    def update_purchase(self, purchase):
        purchase_date, product_id, quantity = purchase

        purchase = self.get_purcahse(purchase_date, product_id)

        if purchase:
            purchase.purchase_date = purchase_date
            purchase.product_id = product_id
            purchase.quantity = quantity
            Base.session.commit()
        else:
            print(f"purchase '{purchase_date, product_id}' not found in db!")

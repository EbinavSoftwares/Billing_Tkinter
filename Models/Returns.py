from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey

from Models import Base


class Returns(Base):
    __tablename__ = 'returns'
    return_date = Column(DateTime, default=datetime.now())
    product_id = Column(Integer(), ForeignKey('products.product_id'), primary_key=True)
    quantity = Column(Integer(), nullable=False)

    def __repr__(self):
        return f'returns {self.product_id}'

    @classmethod
    def get_returns(cls, return_date, product_id):
        return Base.session.query(cls).filter_by(return_date=return_date, product_id=product_id).first()

    @staticmethod
    def add_returns(returns):
        return_date, product_id, quantity = returns

        returns = Returns(return_date=return_date, product_id=product_id, quantity=quantity)
        Base.session.add(returns)
        Base.session.commit()

    def delete_returns(self, return_date, product_id):
        returns = self.get_returns(return_date, product_id)

        if returns:
            Base.session.delete(returns)
            Base.session.commit()
        else:
            print(f"returns '{return_date, product_id}' not found in db!")

    def update_returns(self, returns):
        return_date, product_id, quantity = returns

        returns = self.get_returns(return_date, product_id)

        if returns:
            returns.return_date = return_date
            returns.product_id = product_id
            returns.quantity = quantity
            Base.session.commit()
        else:
            print(f"returns '{return_date, product_id}' not found in db!")

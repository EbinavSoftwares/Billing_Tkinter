from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Float

from Models import Base


class Billing(Base.dec_base):
    __tablename__ = 'billing'

    bill_number = Column(Integer(), primary_key=True)
    bill_date = Column(DateTime, default=datetime.now())
    amount = Column(Float(5, 2), nullable=False)
    discount = Column(Float(5, 2), default=0)
    bill_amount = Column(Float(5, 2), nullable=False)

    def __repr__(self):
        return f'billing {self.bill_number}'

    @classmethod
    def get_bill(cls, bill_number):
        return Base.session.query(cls).filter_by(bill_number=bill_number).first()

    @classmethod
    def get_all_bills(cls):
        return Base.session.query(cls).all()

    @classmethod
    def search_bills(cls, bill_number=None, bill_date=None):
        if bill_number:
            return cls.get_bill(bill_number)

        return Base.session.query(cls).filter(
            Billing.bill_date.like(f'%{bill_date}%')
        ).all()

    @staticmethod
    def create_bill(bill):
        bill_date, amount, discount, bill_amount = bill
        amount = float(amount) + discount
        bill = Billing(bill_date=bill_date, amount=amount, discount=discount, bill_amount=bill_amount)
        Base.session.add(bill)
        Base.session.commit()

        return bill.bill_number

    def delete_bill(self, bill_number):
        bill = self.get_bill(bill_number)

        if bill:
            Base.session.delete(bill)
            Base.session.commit()
        else:
            print(f"bill_number '{bill_number}' not found in db!")

    def update_bill(self, bill):
        bill_number, bill_date, amount, discount, bill_amount = bill

        bill = self.get_product(bill_number)

        if bill:
            bill.bill_date = bill_date
            bill.amount = amount
            bill.discount = discount
            bill.bill_amount = bill_amount
            Base.session.commit()
        else:
            print(f"bill_number '{bill_number}' not found in db!")

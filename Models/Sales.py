from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, func

from Models import Base


class Sales(Base.dec_base):
    __tablename__ = 'sales'
    sales_date = Column(DateTime, default=datetime.now())
    bill_number = Column(Integer(), ForeignKey('billing.bill_number'), primary_key=True)
    product_id = Column(Integer(), ForeignKey('products.product_id'), primary_key=True)
    quantity = Column(Integer(), nullable=False)
    amount = Column(Float(5, 2), nullable=False)
    # billing = relationship('Billing')
    # products = relationship('Product')

    def __repr__(self):
        return f'sales {self.bill_number}'

    @classmethod
    def get_sales(cls, bill_number):
        return Base.session.query(cls).filter_by(bill_number=bill_number).all()

    @staticmethod
    def add_sales(sale):
        sales_date, bill_number, product_id, quantity, amount = sale

        sale = Sales(sales_date=sales_date, bill_number=bill_number, product_id=product_id, quantity=quantity,
                     amount=amount)
        Base.session.add(sale)
        Base.session.commit()

    def delete_sales(self, bill_number):
        sales = self.get_sales(bill_number)

        if sales:
            for sale in sales:
                Base.session.delete(sale)
                Base.session.commit()
        else:
            print(f"bill_number '{bill_number}' not found in db!")

    @classmethod
    def sales_report_daily(cls):
        return Base.session.query(func.strftime('%d-%m-%Y', Sales.sales_date).label("sales_date"),
                                  Sales.product_id,
                                  func.sum(Sales.quantity).label("quantity")
                                  ).group_by(
            func.strftime('%d-%m-%Y', Sales.sales_date),
            Sales.product_id
        ).all()  # .having(func.strftime('%d-%m-%Y', Sales.sales_date) == sales_date)

    @classmethod
    def sales_report_monthly(cls):
        return Base.session.query(func.strftime('%m-%Y', Sales.sales_date).label("sales_month"),
                                  Sales.product_id,
                                  func.sum(Sales.quantity).label("quantity")
                                  ).group_by(
            func.strftime('%m-%Y', Sales.sales_date),
            Sales.product_id
        ).all()

    # @classmethod
    # def update_sales(cls, sale):
    #     bill_number, bill_date, amount, discount, bill_amount = sale
    #
    #     bill = cls.get_product(bill_number)
    #
    #     if bill:
    #         bill.bill_date = bill_date
    #         bill.amount = amount
    #         bill.discount = discount
    #         bill.bill_amount = bill_amount
    #         session.commit()
    #     else:
    #         print(f"bill_number '{bill_number}' not found in db!")

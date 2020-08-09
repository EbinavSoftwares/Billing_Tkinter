from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from Models import Base


class User(Base.dec_base):
    __tablename__ = 'users'

    user_id = Column(Integer(), primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    password = Column(String(15), nullable=False)
    secret_question = Column(String(30), nullable=False)
    secret_answer = Column(String(30), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    is_admin = Column(Boolean(), default=False)

    def __repr__(self):
        return f'User {self.username}'

    @classmethod
    def get_user(cls, username):
        return Base.session.query(cls).filter_by(username=username).first()

    @staticmethod
    def create_user(user):
        username, password, secret_question, secret_answer, is_admin = user

        user = User(username=username, password=password, secret_question=secret_question,
                    secret_answer=secret_answer, is_admin=is_admin)
        Base.session.add(user)
        Base.session.commit()

    def delete_user(self, username):
        user = self.get_user(username)

        if user:
            Base.session.delete(user)
            Base.session.commit()
        else:
            print(f"username '{username}' not found in db!")

    @classmethod
    def set_password(cls, username, password):
        user = cls.get_user(username)

        if user:
            user.password = password
            Base.session.commit()
        else:
            print(f"username '{username}' not found in db!")

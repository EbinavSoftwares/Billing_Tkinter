from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dec_base = declarative_base()
engine = create_engine('sqlite:///appdb.db')  # , echo=True)

Session = sessionmaker(bind=engine)
session = Session()

# dec_base.metadata.create_all(engine)

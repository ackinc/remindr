import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Session

# from models import Base

load_dotenv()

engine = create_engine(os.environ["DATABASE_URL"], echo=True, future=True)
session = Session(engine)

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)

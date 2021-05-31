import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

from app.models import Base

load_dotenv()

engine = create_engine(os.environ["DATABASE_URL"], echo=True, future=True)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

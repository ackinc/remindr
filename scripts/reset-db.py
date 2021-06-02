import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine

# to support absolute import of app.models
# wish there was an easy way to relative-import it instead,
#   but there doesn't seem to be
project_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_dir)

from app.models import Base  # noqa: E402 (imports at top of file)

load_dotenv()

engine = create_engine(os.environ["DATABASE_URL"], echo=True, future=True)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

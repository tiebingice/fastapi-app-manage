
from sqlmodel import Field, SQLModel, create_engine
from settings import settings
engine = create_engine(settings.db_url, echo=True)

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from src.config import settings

engine = create_engine(
    url=settings.sync_refer_to_db(),
    echo=True
)
metadata = MetaData()
session_factory = sessionmaker(engine)

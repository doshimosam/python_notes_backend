from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

password = quote_plus("mosam@123")
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{password}@localhost:5432/notes"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

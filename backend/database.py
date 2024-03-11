from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Replace 'yourdbname', 'yourusername', and 'yourpassword' with your actual database credentials
DATABASE_URL = "postgresql://yourusername:yourpassword@localhost/yourdbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
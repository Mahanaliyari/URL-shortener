import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker



env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)
DATABASE_URL = os.getenv("DATABASE_URL")


if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set. Check your .env file.")

engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autoflush= False, autocommit = False, bind = engine)
Base = declarative_base()
print("Database connection succeded")

def get_db(): 
    db = session_local()
    try: 
        yield db
    finally: 
        db.close()
        
    

from sqlalchemy import Column,Integer,String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

# Defining Database table
class URL(Base): 
    __tablename__ = "url"
    
    id = Column(Integer,nullable= False, primary_key= True)
    original_url = Column(String, nullable= False)
    short_code = Column(String, unique= True, index = True, nullable= False)
    created_at = Column(TIMESTAMP(timezone= True), server_default= text('now()'), nullable= False)
    click_count = Column(Integer, nullable = False, server_default= text('0'))
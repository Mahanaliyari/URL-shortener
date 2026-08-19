import os
from dotenv import load_dotenv
from pydantic import BaseModel, HttpUrl, computed_field
from datetime import datetime


env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)
BASE_URL = os.getenv("BASE_URL")


# Response schema = "what the server sends back"
class URLResponse(BaseModel):
    id: int
    short_code: str
    original_url: str
    created_at: datetime
    click_count: int

    class Config:
        from_attributes = True
        
    ''' Computes (Creates) the "short_url" field, since it does not exist
    as a DB column but we want to return it in our response, 
    so thats why we define it here and we dont have to manually 
    return every field as a response'''
    
    @computed_field
    @property
    def short_url(self) -> str:
        return f"{BASE_URL}/{self.short_code}" 
  
  
  
# Request schema = "what the client sends in"      
class URLCreate(BaseModel): 
    original_url : HttpUrl
    
    
class URLUpdate(BaseModel): 
    original_url : HttpUrl
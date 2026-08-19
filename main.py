import random 
from fastapi import FastAPI,HTTPException,status,Response,Depends
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas 
import string
from .models  import URL
from fastapi.responses import RedirectResponse


models.Base.metadata.create_all(bind = engine)
app = FastAPI()


def generate_short_code(db : Session,length : int = 7) -> str: 
    
    characters = string.ascii_letters + string.digits
    # Loop to generate a unique short code 
    while True: 
        short_code = "".join(random.choices(characters,k= length))
        # filters to find an item with the same short code 
        same_code_item = db.query(URL).filter(URL.short_code == short_code).first()
        if not same_code_item: 
            return short_code
        
        
        
@app.post("/urls", status_code = status.HTTP_201_CREATED,response_model= schemas.URLResponse)
def url_shortener(url:schemas.URLCreate, db: Session = Depends(get_db)):
    
    # unpack and add the entered data to database   
    entered_url = URL(original_url = str(url.original_url),short_code = generate_short_code(db))
    db.add(entered_url)
    db.commit()
    db.refresh(entered_url) 
      
      
    ''' Instead of manually returning every field in our response,
    just because we want to define and return a field
    that is not a column in our Database (short_url),
    we can simply define it in URLResponse pydantic class and 
    we return the whole URL object'''
    # return URLResponse(
    #     id = entered_url.id, # type: ignore
    #     short_code = entered_url.short_code, # type: ignore
    #     short_url =  f"{BASE_URL}/{entered_url.short_code}",
    #     original_url = entered_url.original_url, # type: ignore
    #     created_at= entered_url.created_at, # type: ignore
    #     click_count= entered_url.click_count  # type: ignore
    # )
    
    return entered_url



@app.get("/urls", response_model = list[schemas.URLResponse]) 
def all_urls(db : Session = Depends(get_db)):
    

    # Every item of the list goes through "URLResponse" 
    return db.query(URL).all()   
 
      
        
@app.delete("/urls/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_url(id: int, db: Session = Depends(get_db)):
     
    deleted_url = db.query(URL).filter(URL.id == id)
    
    if not deleted_url.first(): 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"The url with id {id} doesnt exist")
        
    deleted_url.delete(synchronize_session= False)
    db.commit()
    
    return Response(status_code= status.HTTP_204_NO_CONTENT)
    
    

@app.patch("/urls/{id}", response_model = schemas.URLResponse)
def update_url(id: int, url_to_update:schemas.URLUpdate, db: Session = Depends(get_db)): 
    
    updated_url = db.query(URL).filter(URL.id == id).first()
    if not updated_url: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"The url with id {id} doesnt exist")
    
    # Updating only the original_url data field (Patch)
    updated_url.original_url = str(url_to_update.original_url) # type: ignore
    db.commit()
    db.refresh(updated_url)
    
    return updated_url



@app.get("/urls/{id}",response_model= schemas.URLResponse)
def get_statistics(id : int, db : Session = Depends(get_db)):
    get_url = db.query(URL).filter(URL.id == id).first()
    if not get_url:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                                    detail= f"The url with id {id} doesnt exist")
        
    return get_url 


    
    
@app.get("/{short_code}")
def retrieve_url(short_code: str, db : Session = Depends(get_db)): 
    
    ''' This is an URL object which returns all the columns defind in the URL class 
    as a JSON response, if there are no any errors '''
    
    og_url = db.query(URL).filter(URL.short_code == short_code).first()
    if not og_url:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"The url with short code {short_code} doesnt exist")
        
    og_url.click_count += 1  # type: ignore
    db.commit() 
    
    ''' This says : "redirect the browser to whatever this database row's original URL is"
    It does not return any json, it returns a url location that tells the browser to redirect 
    the user to that location '''
    return RedirectResponse(url = og_url.original_url, status_code= 302) # type: ignore





        
    
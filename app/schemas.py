from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class URLCreate(BaseModel):
    url:HttpUrl  

class URLResponse(BaseModel):
    short_url:str

class URLStats(BaseModel):
    original_url:str
    short_code:str
    clicks:int
    created_at:datetime
    expires_at:Optional[datetime]=None

    class Config:
        from_attributes=True  
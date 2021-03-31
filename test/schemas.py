from typing import List, Optional


from pydantic import BaseModel




class ItemBase(BaseModel):

    title: str

    description: Optional[str] = None




class ItemCreate(ItemBase):

    pass



class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True



class UserBase(BaseModel):

    email: str




class UserCreate(UserBase):

    
    password: str
    username: str
    business_account:str
    company_name:Optional[str]

class UserUpdate(UserBase):
    email: str
    password: Optional[str]
    tries: Optional[int]

class User(UserBase):
    id: int
    username: str
    tries:int
    access_token: str
    access_token_type: str
    business_account:str
    company_name:Optional[str]
    #items: List[Item] = []

    class Config:
        orm_mode = True


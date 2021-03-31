from sqlalchemy.orm import Session
import bcrypt
from passlib.context import CryptContext

from . import models, schemas




#def get_user(db: Session, user_id: int):

 #   return db.query(models.User).filter(models.User.id == user_id).first()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):

    return db.query(models.User).filter(models.User.email == email).first()


def update_access_token(db:Session,username,token,token_type):
    
    current_user = db.query(models.User).filter_by(username=username).first()
    current_user.access_token = token
    current_user.access_token_type = token_type
    db.commit()
    

def get_users(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_username(db: Session,username):
    return db.query(models.User).filter_by(username=username).first()


def delete_users(db: Session):
    db.query(models.User).delete()
    db.commit()
    
def delete_user_by_username(db:Session, username):
    db.query(models.User).filter_by(username=username).delete()
    db.commit()
def create_user(db: Session, user: schemas.UserCreate):
    #fake_hashed_password = user.password + "notreallyhashed"
    hashed_password = pwd_context.hash(user.password)
    #business_account = user.business_account
    
    initial_tries = 0
    db_user = models.User(email=user.email, hashed_password=hashed_password,username = user.username,tries = initial_tries,business_account = user.business_account,company_name = user.company_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    #print(db)
    return db_user

def update_tries(db: Session, user: schemas.UserCreate):
    #initial_tries = models.User(tries)
    
    #updated_tries = db1
    current_user = db.query(models.User).filter_by(email=user.email).first() 
    current_tries = current_user.tries
    #print(current_user.username)
    #print(current_tries)
    current_user.tries = current_tries+1
    #print(current_user.tries)
    #db.add(db_user)
    db.commit()
    #db.refresh(db_user)
    return db.query(models.User).filter_by(email=user.email).first()


#def get_items(db: Session, skip: int = 0, limit: int = 100):

 #   return db.query(models.Item).offset(skip).limit(limit).all()



#def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
 #   db_item = models.Item(**item.dict(), owner_id=user_id)
 #   db.add(db_item)
 #   db.commit()
 #   db.refresh(db_item)
 #   return db_item


from typing import List
from . import models, schemas
#from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
import re
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

#from inference3 import set_arguments,convert
#from synthesize import text_to_wav
#from text_to_ssml import text_to_ssml
#from news import getNews
import requests
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200

# pydantic models

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    
class AudioInputs(BaseModel):
    speakerId: str
    textScript : str
    speed : float

class AudioUrl(BaseModel):
	audioUrl:str

class NewsInputs(BaseModel):
    speakerId: str
    category: str
    speed: float
    num_news: int

class UrlList(BaseModel):
    urlList: list

class VidCreateInputs(BaseModel):
    inputUrls = list

class VideoInputs(BaseModel):
    audioUrl : str
    actorId: Optional[str]

class VideoUrl(BaseModel):
    videoUrl: str

class UserName(BaseModel):
    username:str	

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


#def get_user(db, username: str):
 #   if username in db:
  #      user_dict = db[username]
   #     return UserInDB(**user_dict)


def authenticate_user( username: str, password: str,db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    print(user)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=43200)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


#async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
#    if current_user.disabled:
#        raise HTTPException(status_code=400, detail="Inactive user")
#    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = authenticate_user( form_data.username, form_data.password,db)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    crud.update_access_token(db,user.username,access_token,"bearer")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)

def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username Already in use")
    return crud.create_user(db=db, user=user)

@app.delete("/delete/")
async def delete_entries(payload: UserName,db: Session = Depends(get_db)):

    username = payload.username
    if username == "all":
        crud.delete_users(db)
    else:
        crud.delete_user_by_username(db,username)
    raise HTTPException(status_code=200, detail = "Data deleted successfully")

@app.get("/users/", response_model=List[schemas.User])

def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    users = crud.get_users(db, skip=skip, limit=limit)
    #print(users)
    return users
@app.get("/audio")
def getSpeaker(current_user: models.User = Depends(get_current_user)):
    speaker = [{"Voice":"Indian English Female Voice 1","Gender":"Female"},{"Voice":"Indian English Female Voice 2","Gender":"Female"}, {"Voice":"Indian English Male Voice 1","Gender":"Male"},{"Voice":"Hindi Female Voice 1","Gender":"Female"},{"Voice":"Hindi Female Voice 2","Gender":"Female"},{"Voice":"French Female Voice 1","Gender":"Female"},{"Voice":"French Female Voice 2","Gender":"Female"},{"Voice":"French Female Voice 3","Gender":"Female"}]
    #response_object = {"Speakers Key" : speaker}
    return speaker


@app.post("/audio", response_model=AudioUrl, status_code=200)
def getAudioUrl(payload: AudioInputs, current_user: models.User = Depends(get_current_user)):
    if current_user.tries >= 5:
        raise HTTPException(status_code=400, detail = "Quota Exceeded")
        
    speakerId = payload.speakerId
    textScript = payload.textScript
    speed = payload.speed
    #extra stuff

    #audio_name = 'example.wav'
    #audio_url = "/var/www/buildar.in/public_html/audio/"+audio_name
    audioUrl = text_to_wav(speakerId,textScript,speed)

    if not audioUrl:
        raise HTTPException(status_code=400, detail="Model not found.")

    response_object = {"audioUrl": audioUrl}
    current_user.tries = current_user.tries+1
    return response_object

    
@app.get("/news_category")
def news_categories():
    category = [{"0":"national"},{"1":"business"}, {"2":"sports"},{"3":"world"},{"4":"politics"},{"5":"technology"},{"6":"startup"},{"7":"entertainment"},{"8":"science"},{"9":"automobile"}]
    #response_object = {"Speakers Key" : speaker}
    return category    

    

@app.post("/news",response_model = UrlList, status_code = 200)
def getNewsUrl(payload: NewsInputs):
    speakerId = payload.speakerId
    category = payload.category
    speed = payload.speed
    num_news = payload.num_news
    
    speaker = "Male"
    if "Female" in speakerId:
       speaker="Female"
    news_list = []
    diction = getNews(category)
    data = diction['data']
    for i in range(num_news):
       a= data[i]['content']
       string1_protected = re.sub(r"(\d)\.(\d)", r"\1[PROTECTED_DOT]\2", a)
       lines_protected = [line + "." for line in string1_protected.split(".") if line]
       textScript = [line.replace("[PROTECTED_DOT]", ".") for line in lines_protected]
       #textScript= a.split('.')[0]
       textScript = textScript[0]+"~~"
       ssml_text = text_to_ssml(textScript)
       audioUrl = text_to_wav(speakerId,ssml_text,speed,cat = "news")
       if not audioUrl:
          raise HTTPException(status_code=400, detail="Model not found.")
       #speaker = "Male"
       #if "Female" in speakerId[i]:
        #  speaker = "Female"
       dic = {"Url":audioUrl,"image":data[i]["imageUrl"],"speaker":speaker,"title":data[i]['title'],"category":category}
       news_list.append(dic)
       dic={}
    
    #if not audioUrl:
       #raise HTTPException(status_code=400, detail="Model not found.")

    response_object = {"urlList": news_list}
    return response_object

@app.post("/video", response_model=VideoUrl, status_code=200)
async def get_prediction(payload: VideoInputs,current_user: models.User = Depends(get_current_user),db: Session = Depends(get_db)):
    #category = payload.category
    actorId = payload.actorId
    audioUrl = payload.audioUrl
    if current_user.tries >= 5000:
        raise HTTPException(status_code=400, detail = "Quota Exceeded")
    videoEndPoint = 'http://buildar1.ngrok.io/video'
    if current_user.business_account == 'No':
        inputJson = {"category":"public","audioUrl":audioUrl,"actorId":actorId}
        responseObj = requests.post(videoEndPoint, json = inputJson)
    else:
        inputJson = {"category":"private","audioUrl":audioUrl,"companyName":current_user.company_name}
        responseObj = requests.post(videoEndPoint, json = inputJson)
    #Sprint(current_user.username)
    crud.update_tries(db=db, user=current_user)
    final_response = responseObj.json()
    response_object = {"videoUrl":final_response['videoUrl']}
    return response_object
    


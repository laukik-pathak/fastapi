from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
#from datetime import datetime, timedelta

app = FastAPI()
ALGORITHM = "HS256"
SECRET_KEY = "My secret key"
#Access_Token_Expire_Minutes = 30

#OAuth2 schema
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#fake db
fake_db = {"Alice":{"username":"Alice","password":"12345678" }}

def create_token(data: dict):
    token = jwt.encode(data, SECRET_KEY, algorithm = ALGORITHM)
    return token

def authenticate_user(username:str, password:str):
    user = fake_db.get(username)
    if not user or user["password"] != password:
        return None
    return user 

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail = "wrong credentials")
    token = create_token({"sub":user["username"]})
    return {"access token":token, "access_type": "Bearer"}
    
@app.get("/welcome")
async def welcome(token : str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail = "Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail = "Invalid token")
    return {"message": f"Welcome {username}"}



        



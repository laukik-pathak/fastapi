from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from models import User, Base
#use Basemodel, it is a best practice
from pydantic import BaseModel, Field

class UserModel(BaseModel):
    name: str= Field(...,max_length=50)
    email: str

db_url = "sqlite:///./test.db"
engine = create_engine(db_url, echo = True)
SessionLocal = sessionmaker(autoflush = False, autocommit = False, bind = engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

@app.post("/postuser")
async def create_user(user: UserModel, db : Session = Depends(get_db)):
    new_user = User(name = user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/getuser/{id}")
async def get_user(id:int, db:Session= Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    return user

@app.get("/getuser")
async def get_all_users(db:Session = Depends(get_db)):
    user = db.query(User).all()
    return user

@app.put("/putuser/{id}")
async def put_user(id:int ,name:str,email:str, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id ==id).first()
    if user:
        user.name = name
        user.email = email
        db.commit()
        db.refresh(user)
    return user

@app.delete("/deleteuser/{id}")
async def delete_user(id:int, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user:
        db.delete(user)
        db.commit()
    return {"deleted":bool(user)}
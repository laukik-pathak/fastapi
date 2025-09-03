from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
#uvicorn basicCrud:app --reload --port 8080

# These are notes for basic FastAPI with dictionary as database
#Peole and their salary, id is treated as primary key

#App initialization
app = FastAPI()

#Defining the schema for pydantic 
class Person(BaseModel):
    id : int
    name : str =Field(min_length=3)
    salary : float= Field(gt=0) #gt greater than, lt less than default etc can be fields

#dictionary as db
people = dict()


#Basic CRUD Operations

@app.post("/postPerson")
async def save_person(person:Person):
    if person.id not in people:
        people[person.id] = person
        return {"message":"person added to list", "person":person}
    else:
        return{"message":"id is primary key, already exists"}

@app.get("/getPerson")
async def show_person():
    return {"people":people}

@app.put("/putPerson")
async def editPerson(person:Person):
    if person.id in people:
        people[person.id] = person
        return {"message":"person edited"}
    else:
        return {"message": "person with this id is not present in the list"}

@app.delete("/deletePerson/{id}")
async def deletePerson(person:Person):
    people.pop(person.id)
    return {"message":" Person deleted"}



#Dependency function example with depends

#If you want person to show by id in the path
"""def printSalary(id:int =Path(...)):
    if id in people :
        return people[id]
    return "user not found"

@app.get("/getSalary/{id}")
async def getSalary(person = Depends(printSalary(id))):
    return {"message": "Here are the details", "person":person}"""


#If you are using query parameter

def printSalary(id:int, name:str):
    if id in people and people[id].name == name:
        return people[id]
    return "user not found"
@app.get("/getSalary")
async def getSalary(person = Depends(printSalary)):
    return {"message": "Here are the details", "person":person}


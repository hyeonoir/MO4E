from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class CreateIn(BaseModel):
    id: int
    name: str
    age: int
    role: str


class CreateOut(BaseModel):
    status: str
    id: int

# Create a FastAPI instance
app = FastAPI()

# User database
USER_DB = {}

# Fail response
ID_NOT_FOUND = HTTPException(status_code=400, detail="id not found.")

@app.get("/users/all")
def select_asterisk():
    return USER_DB

@app.post("/users", response_model=CreateOut)
def create_user(user: CreateIn):
    temp_dict = {}
    temp_dict["name"] = user.name
    temp_dict["age"] = user.age
    temp_dict["role"] = user.role
    USER_DB[user.id] = temp_dict
    user_dict = {}
    user_dict["status"] = "success"
    user_dict["id"] = len(USER_DB)
    return user_dict


@app.get("/users")
def read_user(id: int):
    if id not in USER_DB:
        raise ID_NOT_FOUND
    return {"nickname": USER_DB[id]}


@app.put("/users")
def update_user(id: int, name: str = 0, age: int = 0, role: str = 0):
    if id not in USER_DB:
        raise ID_NOT_FOUND
    temp_dict = {"name": name, "age": age, "role": role}
    if any(temp_dict.values()):
        for k in temp_dict:
            if temp_dict[k] != 0:
                USER_DB[id][k] = temp_dict[k]

    return {"status": "success"}


@app.delete("/users")
def delete_user(id: str):
    if id not in USER_DB:
        raise ID_NOT_FOUND
    del USER_DB[id]
    return {"status": "success"}

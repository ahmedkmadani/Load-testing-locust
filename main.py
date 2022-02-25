from email.errors import HeaderParseError
import time
from typing import List
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, Header, HTTPException, Depends


app = FastAPI()

@app.get('/hello')
def hello():
    return 'Hello world'


username = 'username'
password = 'password'
token = 'this-is-a-secret-token'

def verify_user(login_token: str = Header(...)):
    if login_token != token :
        raise HTTPException(status_code=401, detail='who are you?')

class LoginData(BaseModel):
    username: str
    password: str


@app.post('/login')
def login(request: LoginData):
    if request.username == username and request.password == password:
        return {'sucess': True, 'token': token}
    return {'sucess': False, token: ''}


@app.get('/logout')
def logout():
    return {'sucess': True, 'message': 'sucess to logout'}


@app.get('/slow', dependencies=[Depends(verify_user)])
def slow():
    time.sleep(3)
    return 'this is such slow endpoint'


@app.get('/fast', dependencies=[Depends(verify_user)])
def fast():
    time.sleep(1)
    return 'this is such fast endpoint'

@app.get('/double-me/{num}', dependencies=[Depends(verify_user)])
def double_me(num: int):
    doubled = num * 2
    return {'request': num, 'response': doubled}


class SquareMeData(BaseModel):
    num: int
    nums : List[int] = [0,1,2]


@app.post('/squre-me', dependencies=[Depends(verify_user)])
def squre_me(request: SquareMeData):
    num_squared = request.num ** 2
    nums_squared = [n ** 2 for n in request.nums]
    res = SquareMeData(num=num_squared, nums=nums_squared)
    return {'request': request.json(), 'resposne': res.json()}


if __name__ == '__main__':
    uvicorn.run(app)

import uvicorn
from fastapi import FastAPI


app = FastAPI()

@app.get('/hello')
def hello():
    return 'Hello world'


if __name__ == '__main__':
    uvicorn.run(app)

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('items/{item_id}')
async def read_item(item_id):
    return {'item_id': item_id}

@app.get('/')
async def root():
    return {"message": "Hello, world!"}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
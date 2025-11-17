from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def index():
  return {"hello": "world"}

@app.get("/health")
async def health():
  return {"status": "ok"}

@app.get("/add")
async def add(x: int, y: int):
  result = x + y
  return {
    "result": result
  }

@app.get("/multiply")
async def multiply(x: int, y: int):
  result = x * y
  return {
    "result": result
  }
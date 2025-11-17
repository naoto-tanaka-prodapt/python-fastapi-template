from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def index():
  return {"hello": "world"}

@app.get("/health")
async def health():
  return {"status": "ok"}
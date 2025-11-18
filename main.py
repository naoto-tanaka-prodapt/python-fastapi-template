from fastapi import FastAPI, HTTPException

app = FastAPI()

jobs_data = {
    "acme": [
      {
        "title": "Customer Support Executive",
        "descrition": "Customer Support"
      },
      {
        "title": "Project Manager",
        "descrition": "Project Management"
      }
    ],
    "bcg": [
      {
        "title": "Technical Architect",
        "descrition": "Architect"
      },
      {
        "title": "Junior Sowtware Engineer",
        "descrition": "Junior Sowtware Engineer"
      }
    ],
    "atlas": [
      {
        "title": "Technical Architect",
        "descrition": "Architect"
      },
      {
        "title": "Junior Sowtware Engineer",
        "descrition": "Junior Sowtware Engineer"
      }
    ]
  }

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

@app.get("/job-board/{company_name}")
async def get_jobs(company_name: str):
  try: 
    jobs = jobs_data[company_name]
  except:
    raise HTTPException(status_code=404, detail="Company not found")
  
  return jobs
from fastapi import FastAPI, HTTPException, Request
from routers import admin_router, metrics_router
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(admin_router.router, prefix="")
app.include_router(metrics_router.router, prefix="/metrics")

company_data = {
    "acme": {
        # "img": "https://img.logo.dev/acme.vc?token=pk_BeIvQp2uTJ2yqPFcwUoAFQ&retina=true",
        "img": "acme.jpg",
        "jobs": [
          {
            "title": "Customer Support Executive",
            "descrition": "Customer Support"
          },
          {
            "title": "Project Manager",
            "descrition": "Project Management"
          }
        ],
    },
    "bcg": {
        # "img": "https://img.logo.dev/bcg.com?token=pk_BeIvQp2uTJ2yqPFcwUoAFQ&retina=true",
        "img": "bcg.jpg",
        "jobs": [
            {
              "title": "Technical Architect",
              "descrition": "Architect"
            },
            {
              "title": "Junior Sowtware Engineer",
              "descrition": "Junior Sowtware Engineer"
            }
        ],
    },
    "atlas": {
        # "img": "https://img.logo.dev/atlascorporation.com?token=pk_BeIvQp2uTJ2yqPFcwUoAFQ&retina=true",
        "img": "atlascorporation.jpg",
        "jobs": [
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

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/app", StaticFiles(directory="frontend/dist"), name="app")
templates = Jinja2Templates(directory="templates")


@app.get("/render/{keyword}", response_class=HTMLResponse)
async def read_item(request: Request, keyword: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"keyword": keyword}
    )


@app.get("/page/{company_name}")
async def get_jobs_page(request: Request, company_name: str):
  """job-board page"""
  try: 
    data = company_data[company_name]
  except:
    raise HTTPException(status_code=404, detail="Company not found")
  
  return templates.TemplateResponse(
        request=request, name="job-boards/job.html", context={"job_list": data["jobs"], "img_url": data["img"]}
    )

@app.get("/api/job-board/{company_name}")
async def get_jobs_api(company_name: str):
  """job-board page"""
  try: 
    data = company_data[company_name]
  except:
    raise HTTPException(status_code=404, detail="Company not found")
  
  return data

# @app.get("/static-job-board.html")
# async def static_job_board():
#     return HTMLResponse(content="<h3>Hello</h3>")
from fastapi import FastAPI, HTTPException, Request
from routers import admin_router, metrics_router
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from db import get_session
from sqlalchemy import text
from models import JobBoard, JobPost

app = FastAPI()
app.include_router(admin_router.router, prefix="")
app.include_router(metrics_router.router, prefix="/metrics")

# company_data = {
#     "acme": {
#         # "img": "https://img.logo.dev/acme.vc?token=pk_BeIvQp2uTJ2yqPFcwUoAFQ&retina=true",
#         "img": "acme.jpg",
#         "jobs": [
#           {
#             "title": "Customer Support Executive",
#             "descrition": "Customer Support"
#           },
#           {
#             "title": "Project Manager",
#             "descrition": "Project Management"
#           }
#         ],
#     },
#     "bcg": {
#         # "img": "https://img.logo.dev/bcg.com?token=pk_BeIvQp2uTJ2yqPFcwUoAFQ&retina=true",
#         "img": "bcg.jpg",
#         "jobs": [
#             {
#               "title": "Technical Architect",
#               "descrition": "Architect"
#             },
#             {
#               "title": "Junior Sowtware Engineer",
#               "descrition": "Junior Sowtware Engineer"
#             }
#         ],
#     },
#     "atlas": {
#         # "img": "https://img.logo.dev/atlascorporation.com?token=pk_BeIvQp2uTJ2yqPFcwUoAFQ&retina=true",
#         "img": "atlascorporation.jpg",
#         "jobs": [
#             {
#               "title": "Technical Architect",
#               "descrition": "Architect"
#             },
#             {
#               "title": "Junior Sowtware Engineer",
#               "descrition": "Junior Sowtware Engineer"
#             }
#           ]
#     }
#   }


@app.get("/")
async def index():
  return {"hello": "world"}

@app.get("/health")
async def health():
  try:
      with get_session() as session:
        session.execute(text("SELECT 1"))
      return {"status": "ok"}
  except Exception as e:
      print(f"Failed to connect: {e}")
      return {"status": "ng"}

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


# @app.get("/page/{company_name}")
# async def get_jobs_page(request: Request, company_name: str):
#   with get_session() as session:
#     job_posts = session.query(JobPost).join(JobBoard, JobPost.job_board_id == JobBoard.id).filter(JobBoard.slug == company_name).all()
  
#   return templates.TemplateResponse(
#         request=request, name="job-boards/job.html", context={"job_list": job_posts, "img_url": data["img"]}
#     )

@app.get("/api/job-boards/{job_board_id}/job-posts")
async def get_jobs_by_job_board_id(job_board_id: int):
  with get_session() as session:
    job_posts = session.query(JobPost).filter(JobPost.job_board_id == job_board_id).all()
    return job_posts

# @app.get("/api/job-board/{company_name}")
# async def get_jobs_api(company_name: str):
#   with get_session() as session:
#     job_posts = session.query(JobPost).join(JobBoard, JobPost.job_board_id == JobBoard.id).filter(JobBoard.slug == company_name).all()
#     return job_posts

@app.get("/api/job-board/{company_name}")
async def get_jobs_api(company_name: str):
  with get_session() as session:
    job_posts = session.query(JobPost).filter(JobPost.job_board.has(JobBoard.slug == company_name)).all()
    return job_posts

@app.get("/api/job-boards")
async def api_job_boards():
  with get_session() as session:
    job_boards = session.query(JobBoard).all()
    return job_boards
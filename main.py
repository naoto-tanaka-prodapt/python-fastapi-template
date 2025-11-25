import os
from typing import Annotated
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from routers import admin_router, metrics_router
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from db import get_session
from sqlalchemy import insert, text
from models import JobBoard, JobPost
from pydantic import BaseModel, Field, field_validator
from file_storage import upload_file
from config import settings

### Schema
class JobBoardForm(BaseModel):
  slug: str = Field(..., min_length=3, max_length=20)
  logo: UploadFile = File(...)

  @field_validator("slug")
  @classmethod
  def to_lowercase(cls, v):
    return v.lower()

app = FastAPI()

# below is for poc
# app.include_router(admin_router.router, prefix="")
# app.include_router(metrics_router.router, prefix="/metrics")

@app.get("/api/health")
async def health():
  try:
      with get_session() as session:
        session.execute(text("SELECT 1"))
      return {"status": "ok"}
  except Exception as e:
      print(f"Failed to connect: {e}")
      return {"status": "ng"}

@app.get("/api/job-boards/{job_board_id}/job-posts")
async def get_jobs_by_job_board_id(job_board_id: int):
  with get_session() as session:
    job_posts = session.query(JobPost).filter(JobPost.job_board_id == job_board_id).all()
    return job_posts

@app.get("/api/job-boards/{company_name}")
async def get_jobs_api(company_name: str):
  with get_session() as session:
    job_posts = session.query(JobPost).filter(JobPost.job_board.has(JobBoard.slug == company_name)).all()
    return job_posts

@app.get("/api/job-boards")
async def api_job_boards():
  with get_session() as session:
    job_boards = session.query(JobBoard).all()
    return job_boards
  
@app.post("/api/job-boards")
async def api_create_new_job_boards(job_board_form: Annotated[JobBoardForm, Form()]):
  logo_contents = await job_board_form.logo.read()
  file_url = upload_file("company-logos", job_board_form.logo.filename, logo_contents, job_board_form.logo.content_type)
  new_job_board = JobBoard(slug=job_board_form.slug, logo_path=file_url)

  with get_session() as session:
    session.add(new_job_board)
    session.commit()
    session.refresh(new_job_board)
  return new_job_board

@app.put("/api/job-boards/{job_board_id}")
async def api_update_job_boards(job_board_id: int, job_board_form: Annotated[JobBoardForm, Form()]):
  with get_session() as session:
    # get record
    target = session.query(JobBoard).filter(JobBoard.id == job_board_id).first()
    if target is None:
      raise HTTPException(status_code=404, detail="Job Board not found")
    
    # file upload
    logo_contents = await job_board_form.logo.read()
    file_url = upload_file("company-logos", job_board_form.logo.filename, logo_contents, job_board_form.logo.content_type)

    # update
    target.slug = job_board_form.slug
    target.logo_path = file_url
    session.commit()
    session.refresh(target)
  return target

# @app.post("/api/job-boards")
# async def api_create_new_job_boards(job_board_form: JobBoardForm):
#   return {"slug": job_board_form.slug}
  
app.mount("/assets", StaticFiles(directory="frontend/build/client/assets"))

if not settings.PRODUCTION:
  app.mount("/uploads", StaticFiles(directory="uploads"))

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
  indexFilePath = os.path.join("frontend", "build", "client", "index.html")
  return FileResponse(path=indexFilePath, media_type="text/html")
 
# @app.post("/multiply")
# async def multiply(x: int, y: int):
#   result = x * y
#   return {
#     "result": result
#   }
# @app.get("/render/{keyword}", response_class=HTMLResponse)
# async def read_item(request: Request, keyword: str):
#     return templates.TemplateResponse(
#         request=request, name="item.html", context={"keyword": keyword}
#     )
import os
from typing import Annotated
from fastapi import FastAPI, Form, HTTPException
from routers import admin_router, metrics_router
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from db import get_session
from sqlalchemy import text
from models import JobApplication, JobBoard, JobPost
from file_storage import upload_file
from config import settings
from utils import create_random_file_name
from schemas import JobApplicationForm, JobBoardForm, JobBoardPatchForm, JobPostForm

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
  
## local file directory
if not settings.PRODUCTION:
  app.mount("/uploads", StaticFiles(directory="uploads"))
  
## JobBoards
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
  _, extension = os.path.splitext(job_board_form.logo.filename)
  file_name_random = create_random_file_name(extension)
  logo_contents = await job_board_form.logo.read()
  file_url = upload_file("company-logos", file_name_random, logo_contents, job_board_form.logo.content_type)
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
    target = session.get(JobBoard, job_board_id)
    if target is None:
      raise HTTPException(status_code=404, detail="Job Board not found")
    
    # file upload
    _, extension = os.path.splitext(job_board_form.logo.filename)
    file_name_random = create_random_file_name(extension)
    logo_contents = await job_board_form.logo.read()
    file_url = upload_file("company-logos", file_name_random, logo_contents, job_board_form.logo.content_type)

    # update
    target.slug = job_board_form.slug
    target.logo_path = file_url
    session.commit()
  return target

@app.patch("/api/job-boards/{job_board_id}")
async def api_patch_job_boards(job_board_id: int, job_board_form: Annotated[JobBoardPatchForm, Form()]):
  with get_session() as session:
    # get record
    target = session.get(JobBoard, job_board_id)
    if target is None:
      raise HTTPException(status_code=404, detail="Job Board not found")
    
    # file upload if logo exist
    if job_board_form.logo:
      _, extension = os.path.splitext(job_board_form.logo.filename)
      file_name_random = create_random_file_name(extension)
      logo_contents = await job_board_form.logo.read()
      file_url = upload_file("company-logos", file_name_random, logo_contents, job_board_form.logo.content_type)
      target.logo_path = file_url

    # file upload if slug exist
    if job_board_form.slug:
      target.slug = job_board_form.slug

    # commit
    session.commit()
    session.refresh(target)
  return target

@app.delete("/api/job-boards/{job_board_id}")
async def api_delete_job_boards(job_board_id: int):
  with get_session() as session:
    # delete record
    target = session.get(JobBoard, job_board_id)
    if target is None:
      raise HTTPException(status_code=404, detail="Job Board not found")
    
    session.delete(target)
    session.commit()
  return {
    "result": "success"
  }

## JobApplications
@app.post("/api/job-applications")
async def api_create_new_job_applications(job_application_form: Annotated[JobApplicationForm, Form()]):
  # check jobpost status
  with get_session() as session:
    target = session.get(JobPost, job_application_form.job_post_id)
    if target is None:
      raise HTTPException(status_code=404, detail="Job Post not found")
    if target.is_open is False:
      raise HTTPException(status_code=400, detail="This job post is already closed")

  # Upload Resume
  _, extension = os.path.splitext(job_application_form.resume.filename)
  file_name_random = create_random_file_name(extension)
  logo_contents = await job_application_form.resume.read()
  file_url = upload_file("resumes", file_name_random, logo_contents, job_application_form.resume.content_type)

  # Create Job Application
  new_job_application = JobApplication(
      job_post_id=job_application_form.job_post_id,
      first_name=job_application_form.first_name,
      last_name=job_application_form.last_name,
      email=job_application_form.email,
      resume_path=file_url
    )
   
  with get_session() as session:   
    session.add(new_job_application)
    session.commit()
    session.refresh(new_job_application)
  return new_job_application

@app.get("/api/job-applications")
async def api_job_applications():
  with get_session() as session:
    job_applications = session.query(JobApplication).all()
    return job_applications
  
## Job Post
@app.patch("/api/job-posts/{job_post_id}/close")
async def close_job_post(job_post_id: int):
  with get_session() as session:
    # get record
    target = session.get(JobPost, job_post_id)
    if target is None:
      raise HTTPException(status_code=404, detail="Job Post not found")
    
    # Change is_open
    target.is_open = False
    session.commit()
  return target

@app.post("/api/job-posts")
async def api_create_new_job_posts(job_post_form: Annotated[JobPostForm, Form()]):
  new_job_post = JobPost(
    job_board_id=job_post_form.job_board_id,
    title=job_post_form.title,
    description=job_post_form.description
  )

  with get_session() as session:
    session.add(new_job_post)
    session.commit()
    session.refresh(new_job_post)
  return new_job_post
  
## For UI
app.mount("/assets", StaticFiles(directory="frontend/build/client/assets"))

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
  indexFilePath = os.path.join("frontend", "build", "client", "index.html")
  return FileResponse(path=indexFilePath, media_type="text/html")
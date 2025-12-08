import os
from typing import Annotated
from fastapi import Depends, Form, HTTPException, APIRouter, BackgroundTasks
from db import get_session
from sqlalchemy import text
from models import JobApplication, JobPost
from file_storage import upload_file
from utils import create_random_file_name
from schemas import JobApplicationForm
from emailer import send_email
from utils import evaluate_resume
from vector_search import ingest_resume_for_recommendataions, get_vector_store

router = APIRouter()

## Job Application
@router.post("/api/job-applications")
async def api_create_new_job_applications(job_application_form: Annotated[JobApplicationForm, Form()],
                                          background_task: BackgroundTasks,
                                          db = Depends(get_session),
                                          vector_store = Depends(get_vector_store)
                                          ):
  # check jobpost status
  target = db.get(JobPost, job_application_form.job_post_id)
  if target is None:
    raise HTTPException(status_code=404, detail="Job Post not found")
  if target.is_open is False:
    raise HTTPException(status_code=400, detail="This job post is already closed")

  # Upload Resume
  _, extension = os.path.splitext(job_application_form.resume.filename)
  file_name_random = create_random_file_name(extension)
  resume_contents = await job_application_form.resume.read()
  file_url = upload_file("resumes", file_name_random, resume_contents, job_application_form.resume.content_type)

  # Create Job Application
  new_job_application = JobApplication(
      job_post_id=job_application_form.job_post_id,
      first_name=job_application_form.first_name,
      last_name=job_application_form.last_name,
      email=job_application_form.email,
      resume_path=file_url
    )
   
  db.add(new_job_application)
  db.commit()
  db.refresh(new_job_application)

  # background_task.add_task(
  #   evaluate_resume,
  #   resume_contents,
  #   target.description,
  #   new_job_application.id
  # )
  
  background_task.add_task(
    ingest_resume_for_recommendataions,
    resume_contents,
    file_name_random,
    new_job_application.id,
    vector_store,
    new_job_application.job_post_id
  )

  background_task.add_task(
    send_email,
    new_job_application.email,
    "Acknowledgement",
    "We have received your job application"
  )

  return new_job_application

@router.get("/api/job-applications")
async def api_job_applications():
  with get_session() as session:
    job_applications = session.query(JobApplication).all()
    return job_applications
  
@router.get("/api/job-applications/{job_application_id}")
async def api_get_job_applications_by_id(job_application_id: int):
  with get_session() as session:
    job_application = session.get(JobApplication, job_application_id)
    if job_application is None:
      raise HTTPException(status_code=404, detail="Job Board not found")
    return job_application
  
@router.put("/api/job-applications/{job_application_id}")
async def api_update_job_applications(job_application_id: int, job_application_form: Annotated[JobApplicationForm, Form()]):
  with get_session() as session:
    # get record
    target = session.get(JobApplication, job_application_id)
    if target is None:
      raise HTTPException(status_code=404, detail="Job Application not found")
    
    # file upload
    _, extension = os.path.splitext(job_application_form.resume.filename)
    file_name_random = create_random_file_name(extension)
    logo_contents = await job_application_form.resume.read()
    file_url = upload_file("resumes", file_name_random, logo_contents, job_application_form.resume.content_type)

    # update
    target.first_name = job_application_form.first_name
    target.last_name = job_application_form.last_name
    target.email = job_application_form.email
    target.resume_path = file_url
    session.commit()
  return target
  
@router.delete("/api/job-applications/{job_application_id}")
async def api_job_applications(job_application_id: int):
  with get_session() as session:
    target = session.get(JobApplication, job_application_id)
    if target is None:
      raise HTTPException(status_code=404, detail="Job Board not found")
    
    session.delete(target)
    session.commit()
  return {
    "result": "success"
  }
  

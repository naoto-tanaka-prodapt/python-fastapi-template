from typing import Annotated
from fastapi import Depends, Form, HTTPException, APIRouter
from db import get_session
from models import JobApplication, JobPost
from schemas import JobPostForm
from vector_search import get_recommendation, get_vector_store

router = APIRouter()

@router.get("/api/job-posts/{job_post_id}")
async def get_job_post(job_post_id: int, db=Depends(get_session)):
  job_post = db.get(JobPost, job_post_id)
  if job_post is None:
    raise HTTPException(status_code=404, detail="Job Post not found")
  if job_post.is_open is False:
    raise HTTPException(status_code=400, detail="This job post is already closed")
  
  job_applications = db.query(JobApplication).filter(JobApplication.job_post_id == job_post_id).all()
  return {
    "job_post": job_post,
    "job_applications": job_applications
  }

@router.patch("/api/job-posts/{job_post_id}/close")
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

@router.post("/api/job-posts")
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

@router.get("/api/job-posts/{job_post_id}/recommend")
async def api_job_post_recommandation(job_post_id: int, db = Depends(get_session), vector_store = Depends(get_vector_store)):
  # get description
  job_post = db.get(JobPost, job_post_id)
  
  # get recommendation
  recommended_applicant = get_recommendation(job_post.description, vector_store)
  recommended_applicant_id = recommended_applicant.metadata["_id"]
  application = db.get(JobApplication, recommended_applicant_id)
  
  return application
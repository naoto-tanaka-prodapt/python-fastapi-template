import os
from typing import Annotated
from fastapi import Form, HTTPException, APIRouter
from db import get_session
from models import JobBoard, JobPost
from file_storage import upload_file
from utils import create_random_file_name
from schemas import JobBoardForm, JobBoardPatchForm

router = APIRouter()

## JobBoards
# @router.get("/api/job-boards/{company_name}")
# async def get_jobs_api(company_name: str):
#   with get_session() as session:
#     job_posts = session.query(JobPost).filter(JobPost.job_board.has(JobBoard.slug == company_name)).all()
#     return job_posts
  
@router.get("/api/job-boards")
async def api_job_boards():
  with get_session() as session:
    job_boards = session.query(JobBoard).all()
    return job_boards
  
@router.get("/api/job-boards/{job_board_id}")
async def api_job_boards_by_id(job_board_id: int):
  with get_session() as session:
    job_board = session.get(JobBoard, job_board_id)
    if job_board is None:
      raise HTTPException(status_code=404, detail="Job Board not found")

    return job_board

@router.get("/api/job-boards/{job_board_id}/job-posts")
async def get_jobs_by_job_board_id(job_board_id: int):
  with get_session() as session:
    job_posts = session.query(JobPost).filter(JobPost.job_board_id == job_board_id).all()
    return job_posts

@router.post("/api/job-boards")
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

@router.put("/api/job-boards/{job_board_id}")
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

@router.patch("/api/job-boards/{job_board_id}")
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

@router.delete("/api/job-boards/{job_board_id}")
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
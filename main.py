import os
from config import settings
from typing import Annotated
from fastapi import FastAPI, Form, HTTPException, Request, Response
from routers import job_application_router, job_board_router, llm_router
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from db import get_session
from sqlalchemy import text
from models import JobPost
from config import settings
from auth import authenticate_admin, AdminAuthzMiddleware, AdminSessionMiddleware, delete_admin_session
from schemas import JobPostForm, AdminLoginForm
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

app.include_router(job_board_router.router)
app.include_router(job_application_router.router)
app.include_router(llm_router.router)

app.add_middleware(AdminAuthzMiddleware)
app.add_middleware(AdminSessionMiddleware)


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

## Auth
@app.post("/api/admin-login")
async def admin_login(response: Response, admin_login_form: Annotated[AdminLoginForm, Form()]):
   auth_response = authenticate_admin(admin_login_form.username, admin_login_form.password)
   if auth_response is not None:
      secure = settings.PRODUCTION
      response.set_cookie(key="admin_session", value=auth_response, httponly=True, secure=secure, samesite="Lax")
      return {}
   else:
      raise HTTPException(status_code="403")
   
@app.get("/api/me")
async def me(req: Request):
  return {"is_admin": req.state.is_admin}

@app.post("/api/admin-logout")
async def admin_logout(request: Request, response: Response):
  delete_admin_session(request.cookies.get("admin_session"))
  secure = settings.PRODUCTION
  response.delete_cookie(key="admin_session", httponly=True, secure=secure, samesite="LaX")
  
## For UI
app.mount("/assets", StaticFiles(directory="frontend/build/client/assets"))

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
  indexFilePath = os.path.join("frontend", "build", "client", "index.html")
  return FileResponse(path=indexFilePath, media_type="text/html")
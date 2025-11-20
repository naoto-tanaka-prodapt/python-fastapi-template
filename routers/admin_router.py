from fastapi import APIRouter, File, UploadFile, Request, Form
from fastapi.templating import Jinja2Templates
from typing import Annotated


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/admin")
async def get_admin_page(request: Request):
  return templates.TemplateResponse(
        request=request, name="job-boards/admin.html"
    )

@router.post("/uploadfile")
async def upload_image(request: Request, company: Annotated[str, Form()], file: UploadFile = File(...)):
    file_name = {
       "acme": "acme.jpg",
       "atlas": "atlascorporation.jpg",
       "bcg": "bcg.jpg"
    }

    file_path = f"static/img/{file_name[company]}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
        # shutil.copyfileobj(file.file, buffer)

    return templates.TemplateResponse(
        "job-boards/admin.html",
        {
            "request": request,
            "filename": file_name[company]
        }
    )
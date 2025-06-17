from fastapi import APIRouter, Depends, HTTPException, responses, File, UploadFile
from model.schemas import *
from sqlalchemy.orm import Session
import os
from repository.file import *
from util.util import *

# ALLOWED_EXTENSIONS = load_allowed_extensions("allowed_extensions.yaml")

ALLOWED_EXTENSIONS = {"pdf", "docx", "pptx"}
KEY = "a234slkdjfgosdi547utbod7sinfl87cvdiyrstn4bol3asuy8d"  # will be changed
router = APIRouter(tags=["file"], prefix="/file")


@router.post("/upload/")
async def upload_file(
    user_id: int,
    access_id: int,
    key: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    file_extension = os.path.splitext(file.filename)[1][1:]
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Not Allowed!")

    file_hash = compute_file_hash(user_id, key, file.filename)

    with open(f"uploads/{file_hash}", "wb") as f:
        content = await file.read()
        f.write(content)

    return file_create_file(
        file_hash=file_hash,
        # access_id=access_id
    )


@router.get("/download/{file_id}")
async def download_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(File).filter(File.id == file_id).first()
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = f"uploads/{db_file.info}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="file not found in server")

    return responses.FileResponse(file_path)

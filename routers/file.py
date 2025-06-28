from fastapi import APIRouter, Depends, HTTPException, responses, File, UploadFile
from logic.file import *
from model.schemas import *
from sqlalchemy.orm import Session
import os
from repository.file import *
from util.util import *

# ALLOWED_EXTENSIONS = load_allowed_extensions("allowed_extensions.yaml")

# ALLOWED_EXTENSIONS = {"pdf", "docx", "pptx"}
# KEY = "a234slkdjfgosdi547utbod7sinfl87cvdiyrstn4bol3asuy8d"  # will be changed
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
    file_extension_allowed(file_extension)

    file_hash = compute_file_hash(user_id, key, file.filename)
    file_hash = write_file_hash(file_hash=file_hash, file=file)
    return file_create_file(
        file_hash=file_hash,
        # access_id=access_id
    )


@router.get("/download/{file_id}")
async def download_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(File).filter(File.id == file_id).first()
    db_file_exist(db_file)

    file_path = f"uploads/{db_file.info}"
    file_path_exists(file_path)
    return responses.FileResponse(file_path)

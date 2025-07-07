from fastapi import HTTPException, File, UploadFile

import os
import aiofiles
from repository.file import *
from util.util import *

ALLOWED_EXTENSIONS = {"pdf", "docx", "pptx"}
KEY = "a234slkdjfgosdi547utbod7sinfl87cvdiyrstn4bol3asuy8d"  # will be changed


def file_extension_allowed(file_extension):
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Not Allowed!")


async def write_file_hash(file_name: str, file: UploadFile):

    os.makedirs("uploads", exist_ok=True)
    async with aiofiles.open(f"uploads/{file_name}", "wb") as f:
        content = await file.read()
        await f.write(content)
    return file_name


def db_file_exist(db_file: File):
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")


def file_path_exists(file_path: str):
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="file not found in server")

from sqlalchemy.sql import exists
from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from fastapi import HTTPException
from datetime import datetime


def file_create_file(
    db: Session,
    file_hash: str,
    created_at: datetime,
):
    db_file = File(info=file_hash, created_at=created_at)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def get_all_files(db: Session):
    return db.query(File).all()

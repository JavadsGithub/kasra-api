from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy import update, desc
from datetime import time

from repository import user
from util import util


router = APIRouter(tags=["supervisor"], prefix="/supervisor")

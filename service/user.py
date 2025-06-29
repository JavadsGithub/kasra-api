from typing import List
from fastapi import HTTPException
from repository.user import *


def reports_exist(reports: List[Report]):
    if not reports:
        raise HTTPException(status_code=404, detail="Reports not found")

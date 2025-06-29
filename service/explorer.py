from fastapi import HTTPException
from model.model import RFP


def rfps_exist(rfps: RFP):
    raise HTTPException(status_code=404, detail="No RFPs found")

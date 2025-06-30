from fastapi import HTTPException
from model.model import RFP, RFPField


def rfps_exist(rfps: RFP):
    if not rfps:
        raise HTTPException(status_code=404, detail="No RFPs found")


def rfp_fields_exist(rfp_fields: RFPField):
    if not rfp_fields:
        raise HTTPException(status_code=404, detail="No RFP fields found")

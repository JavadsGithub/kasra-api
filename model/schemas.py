from typing import Optional
from pydantic import BaseModel
from datetime import date


# login
class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class TokenData(BaseModel):
    username: str | None = None


# # Define UserTypeInfo as needed
# class UserTypeInfo(BaseModel):
#     id: int
#     info: str


# User schemas
class UserAddRequest(BaseModel):
    username: str
    password: str
    fname: str
    lname: str
    father_name: str
    birth: date
    resume_file_id: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    active: bool


class UserUpdateRequest(BaseModel):
    id: int
    username: str
    fname: str
    lname: str
    father_name: str
    birth: date
    resume_file_id: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    active: bool

    class Config:
        from_attributes = True


class UserInfoResponse(BaseModel):
    id: int
    username: str
    fname: str
    lname: str
    father_name: str
    birth: date
    resume_file_id: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    active: bool
    user_type_id: int

    class Config:
        from_attributes = True


# RFPField


class RFPFieldResponse(BaseModel):
    id: int
    title: str


# RFP schemas
class RFPRequest(BaseModel):
    info: str
    RFP_field_id: int
    file_id: Optional[int] = None


class RFPResponse(BaseModel):
    id: int
    info: str
    RFP_field_id: int
    file_id: Optional[int] = None

    class Config:
        from_attributes = True


# Proposal schemas
class ProposalRequest(BaseModel):
    info: str
    RFP_id: int
    user_id: int
    state: int  # ENUM
    comment: str
    file_id: Optional[int] = None


class ProposalResponse(BaseModel):
    id: int
    info: str
    RFP_id: int
    user_id: int
    comment: str
    state: int
    comment: str
    file_id: Optional[int] = None

    class Config:
        from_attributes = True


class ProposalUpdate(BaseModel):
    state: int  # ENUM
    comment: str


# Commission schemas
class CommissionRequest(BaseModel):
    title: str
    comment: str
    state: int  # asking M.E for the best solution of handeling the enum
    proposal_id: int
    user_supervisor_id: int
    user_discoverer_id: int
    file_id: Optional[int] = None


class CommissionResponse(BaseModel):
    id: int
    title: str
    comment: str
    state: int  # also enum, also ask M.E
    proposal_id: int
    user_supervisor_id: int
    user_discoverer_id: int
    file_id: Optional[int] = None

    class Config:
        from_attributes = True


# Project schemas
class ProjectRequest(BaseModel):
    title: str
    proposal_id: int
    user_supervisor_id: int
    user_discoverer_id: int
    user_master_id: int
    user_broker_id: int
    user_user_id: int


class ProjectResponse(BaseModel):
    id: int
    title: str
    proposal_id: int
    user_supervisor_id: int
    user_discoverer_id: int
    user_master_id: int
    user_broker_id: int
    user_user_id: int

    class Config:
        from_attributes = True


# Report schemas
class ReportRequest(BaseModel):
    info: str
    project_id: int
    comment: str
    state: int


class ReportResponse(BaseModel):
    id: int
    info: str
    project_id: int
    comment: str
    state: int

    class Config:
        from_attributes = True


class ReportUpdate(BaseModel):
    state: int
    comment: str


# ReportFile schemas
class ReportFileRequest(BaseModel):
    info: str
    report_id: int
    file_id: int


class ReportFileResponse(BaseModel):
    id: int
    info: str
    report_id: int
    file_id: int

    class Config:
        from_attributes = True

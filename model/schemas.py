import datetime
import enum
from typing import Optional
from pydantic import BaseModel
from datetime import date


class AllocatetState(enum.Enum):
    pending_to_specify_title = "ارجرا جهت تعیین موضوع"
    pending_to_specify_supervisor = "در انتظار انتخاب ناظر"
    pending_to_accept = "در انتطار تایید نهایی"
    eccepted = "تایید شده"
    rejected = "رد شده"


class ProposalState(enum.Enum):
    pending_to_fill = "در انتظار تکمیل"
    pending_to_explorer_accept = "در انتظار تایید کاشف"
    pending_to_accept = "در انتظار تایید نهایی"
    eccepted = "تایید شده"
    rejected = "رد شده"


class ReportState(enum.Enum):
    rejected = "رد شده"
    eccepted = "تایید شده"
    pending = "در انتظار تایید"


class ProjectState(enum.Enum):
    active = "فعال"
    ended = "غیر فعال"
# login


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    role_id: int


class TokenData(BaseModel):
    username: str | None = None


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


class UserMeInfoResponse(BaseModel):
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
    STATE_COMMISSION: dict
    STATE_PROPOSAL: dict

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


class UserInfoLimitedResponse(BaseModel):
    id: int
    fname: str
    lname: str

    class Config:
        from_attributes = True


# RFPField


class RFPFieldResponse(BaseModel):
    id: int
    title: str


# RFP schemas
class ExplorerCreateUpdateRFP(BaseModel):
    info: str
    file_id: Optional[int] = None
    RFP_field_id: int

    class Config:
        orm_mode = True


class RFPResponse(BaseModel):
    id: int
    info: str
    created_at: datetime
    file_id: Optional[int] = None
    creator_id: int
    RFP_field: RFPFieldResponse

    class Config:
        orm_mode = True


# allocate

class BrokerCreateAllocate(BaseModel):
    RFP_id: int
    allocated_to_user_id: int

    class Config:
        orm_mode = True


class UserUpdateAllocate(BaseModel):
    project_title: str
    project_description: str

    class Config:
        orm_mode = True


class BrokerUpdateAllocate(BaseModel):
    supervisor_id: int

    class Config:
        orm_mode = True


class ResearcherUpdateAllocate(BaseModel):
    state: str

    class Config:
        orm_mode = True


class AllocateResponse(BaseModel):
    id: int
    creator_id: int
    created_at: datetime

    RFP: RFPResponse
    allocated_to_user: UserInfoLimitedResponse
    project_title: Optional[str]
    project_description: Optional[str]
    state: str

    class Config:
        orm_mode = True


# Proposal schemas
class ExplorerCreateProposal(BaseModel):
    master_name_and_family: str
    # add title, description and RFP based on Allocate_id

    class Config:
        orm_mode = True


class UserUpdateProposal(BaseModel):
    file_id: int

    class Config:
        orm_mode = True


class ExplorerUpdateProposal(BaseModel):
    comment: str
    supervisor_id: int

    class Config:
        orm_mode = True


class ResearcherUpdateProposal(BaseModel):
    state: str

    class Config:
        orm_mode = True


class UserUpdateProposal(BaseModel):
    file_id: int

    class Config:
        orm_mode = True


class ProposalResponse(BaseModel):
    id: int
    creator_id: int
    created_at: datetime
    master_name_and_family: str
    title: str
    description: str
    RFP_id: int
    allocate_id: Optional[int]  # اگر ممکن است None باشد
    supervisor_id: Optional[int]  # اگر ممکن است None باشد
    user_id: int
    file_id: Optional[int]
    state: ProposalState
    comment: Optional[str]  # اگر ممکن است None باشد

    class Config:
        orm_mode = True

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
    proposal: ProposalSingleResponse
    supervisor: UserInfoLimitedResponse
    discoverer: UserInfoLimitedResponse
    master: UserInfoLimitedResponse
    broker: UserInfoLimitedResponse

    class Config:
        from_attributes = True


# Report schemas
class ReportRequest(BaseModel):
    info: str
    project_id: int
    comment: str
    file_pdf_id: int
    file_docx_id: int
    file_pptx_id: int
    percent: int

    # state: int


class ReportResponse(BaseModel):
    id: int
    creator_id: int
    created_at: datetime

    title: str

    comment: str
    state: str
    anounced_percent: int
    accepted_percent: int
    project_id: int
    file_pdf_id: int
    file_docx_id: int
    file_pptx_id: int
    project: ProjectResponse

    class Config:
        from_attributes = True


class ReportUpdate(BaseModel):
    state: str
    comment: str


# # ReportFile schemas
# class ReportFileRequest(BaseModel):
#     info: str
#     report_id: int
#     file_id: int


# class ReportFileResponse(BaseModel):
#     id: int
#     info: str
#     report: ReportResponse
#     file_id: int

#     class Config:
#         from_attributes = True

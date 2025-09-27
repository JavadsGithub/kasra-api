from ast import Str
import enum
from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime

# allocate_state = {
#     "اجرا جهت تعیین موضوع", "در انتظار انتخاب ناظر", "در انتطار تایید نهایی", "تایید شده", "رد شده", }
# proposal_state = {
#     "در انتظار تکمیل", "در انتظار تایید کاشف", "در انتظار تایید نهایی", "تایید شده", "رد شده", }
# reportt_state = {
#     "رد شده", "تایید شده", "در انتظار تایید", }
# project_state = {
#     "فعال", "غیر فعال", }


# class AllocatetState(enum.Enum):
#     pending_to_specify_title = "اجرا جهت تعیین موضوع"
#     pending_to_specify_supervisor = "در انتظار انتخاب ناظر"
#     pending_to_accept = "در انتطار تایید نهایی"
#     eccepted = "تایید شده"
#     rejected = "رد شده"


# class ProposalState(enum.Enum):
#     pending_to_fill = "در انتظار تکمیل"
#     pending_to_explorer_accept = "در انتظار تایید کاشف"
#     pending_to_accept = "در انتظار تایید نهایی"
#     eccepted = "تایید شده"
#     rejected = "رد شده"


# class ReportState(enum.Enum):
#     rejected = "رد شده"
#     eccepted = "تایید شده"
#     pending = "در انتظار تایید"


# class ProjectState(enum.Enum):
#     active = "فعال"
#     ended = "غیر فعال"
# login

class MasterResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MasterRequest(BaseModel):
    # id: int
    name: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    role_id: int


class TokenData(BaseModel):
    username: str | None = None


class NotificationResponse(BaseModel):
    id: int
    owner: int
    created_at: datetime
    title: str

    class Config:
        from_attributes = True


# User schemas
class UserAddRequest(BaseModel):
    username: str
    password: Optional[str] = None
    user_type_id: int
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


class UserRoleResponse(BaseModel):
    id: int
    title: str

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
    notification_count: int
    allocate_state: dict
    proposal_state: dict
    report_state: dict
    project_state: dict

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
    beneficiary: Optional[str] = None  # کاربر بهره‌بردار
    representative: Optional[str] = None  # نماینده بهره‌بردار
    issue_title: Optional[str] = None  # عنوان مسئله
    issue_description: Optional[str] = None  # شرح مختصر مسئله
    mission_area: Optional[str] = None  # حوضه ماموریتی
    specialty_field: Optional[str] = None  # رشته و گرایش تخصصی
    issue_origin: Optional[str] = None  # توضیحات درباره منشا یافتن مسئله
    proposed_execution_path: Optional[str] = None  # توضیحات مسیر پیشنهادی اجرا
    frequency: Optional[str] = None  # فراوانی
    financial_value: Optional[str] = None  # ارزش مالی مسئله
    key_requirements: Optional[str] = None  # الزامات کلیدی و حیاتی
    limitations: Optional[str] = None  # محدودیت ها
    technical_solution: Optional[str] = None  # راه حل فنی
    related_projects: Optional[str] = None  # پروژه های مرتبط
    proposed_product: Optional[str] = None  # محصول پیشنهادی
    issue_support: Optional[str] = None  # نحوه حمایت از مسئله
    analyst_evaluator: Optional[str] = None  # تحلیل کارگزار کاشف
    keywords: Optional[str] = None  # کلمات کلیدی

    class Config:
        orm_mode = True


class RFPResponse(BaseModel):
    id: int
    info: str
    created_at: datetime
    creator_id: int
    creator: UserInfoLimitedResponse
    file_id: Optional[int] = None
    beneficiary: Optional[str] = None  # کاربر بهره‌بردار
    representative: Optional[str] = None  # نماینده بهره‌بردار
    issue_title: Optional[str] = None  # عنوان مسئله
    issue_description: Optional[str] = None  # شرح مختصر مسئله
    mission_area: Optional[str] = None  # حوضه ماموریتی
    specialty_field: Optional[str] = None  # رشته و گرایش تخصصی
    issue_origin: Optional[str] = None  # توضیحات درباره منشا یافتن مسئله
    proposed_execution_path: Optional[str] = None  # توضیحات مسیر پیشنهادی اجرا
    frequency: Optional[str] = None  # فراوانی
    financial_value: Optional[str] = None  # ارزش مالی مسئله
    key_requirements: Optional[str] = None  # الزامات کلیدی و حیاتی
    limitations: Optional[str] = None  # محدودیت ها
    technical_solution: Optional[str] = None  # راه حل فنی
    related_projects: Optional[str] = None  # پروژه های مرتبط
    proposed_product: Optional[str] = None  # محصول پیشنهادی
    issue_support: Optional[str] = None  # نحوه حمایت از مسئله
    analyst_evaluator: Optional[str] = None  # تحلیل کارگزار کاشف
    keywords: Optional[str] = None  # کلمات کلیدی

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


class ExplorerUpdateAllocate(BaseModel):
    master_id: int

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

    rfp: RFPResponse
    allocated_to_user: UserInfoLimitedResponse
    project_title: Optional[str] = None
    project_description: Optional[str] = None
    master: Optional[MasterResponse] = None
    state: str

    class Config:
        orm_mode = True


# Proposal schemas
class ExplorerCreateProposal(BaseModel):
    master_id: int
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
    commission_file_id: Optional[int] = None
    commission_date_time: Optional[datetime] = None

    class Config:
        orm_mode = True


class SupervisorUpdateProposal(BaseModel):
    comment: str
    supervisor_id: int
    commission_file_id: Optional[int] = None
    commission_date_time: Optional[datetime] = None

    class Config:
        orm_mode = True


class ResearcherUpdateProposal(BaseModel):
    state: str

    class Config:
        orm_mode = True


class UserUpdateProposal(BaseModel):
    file_id: int
    start_at: datetime
    end_at: datetime

    price: Optional[str] = None
    applicant_name: Optional[str] = None  # نام و نام خانوادگی مجری
    contact_number: Optional[str] = None  # شماره تماس
    education: Optional[str] = None  # مدرک تحصیلی
    expertise: Optional[str] = None  # تخصص
    project_duration: Optional[str] = None  # مدت‌زمان و نفرساعت اجرای پروژه
    project_goals: Optional[str] = None  # اهداف پروژه
    project_importance: Optional[str] = None  # اهمیت پروژه
    technical_details: Optional[str] = None  # جزئیات و روش های فنی انجام پروژه
    # ويژگي‌هاي اصلي و مشخصات عمومی و فني محصول پروژه
    product_features: Optional[str] = None
    # سوابق پژوهش‌ها و محصولات مشابه موجود در سطح کشور و دنیا
    similar_products: Optional[str] = None
    project_outcomes: Optional[str] = None  # دستاوردهای هر گام از پروژه
    project_innovation: Optional[str] = None  # نوآوری پروژه
    # ریسک‌ها و گلوگاه‌هاي احتمالی در اجرای پروژه
    project_risks: Optional[str] = None

    class Config:
        orm_mode = True


class ProposalResponse(BaseModel):
    id: int
    creator_id: int
    created_at: datetime
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    master: Optional[MasterResponse] = None
    title: str
    # description: str
    RFP_id: int
    allocate_id: Optional[int] = None  # اگر ممکن است None باشد
    supervisor_id: Optional[int] = None  # اگر ممکن است None باشد
    user_id: int
    file_id: Optional[int] = None
    state: str
    comment: Optional[str] = None  # اگر ممکن است None باشد

    applicant_name: Optional[str] = None  # نام و نام خانوادگی مجری
    contact_number: Optional[str] = None  # شماره تماس
    education: Optional[str] = None  # مدرک تحصیلی
    expertise: Optional[str] = None  # تخصص
    project_duration: Optional[str] = None  # مدت‌زمان و نفرساعت اجرای پروژه
    project_goals: Optional[str] = None  # اهداف پروژه
    project_importance: Optional[str] = None  # اهمیت پروژه
    technical_details: Optional[str] = None  # جزئیات و روش های فنی انجام پروژه
    # ويژگي‌هاي اصلي و مشخصات عمومی و فني محصول پروژه
    product_features: Optional[str] = None
    # سوابق پژوهش‌ها و محصولات مشابه موجود در سطح کشور و دنیا
    similar_products: Optional[str] = None
    project_outcomes: Optional[str] = None  # دستاوردهای هر گام از پروژه
    project_innovation: Optional[str] = None  # نوآوری پروژه
    # ریسک‌ها و گلوگاه‌هاي احتمالی در اجرای پروژه
    project_risks: Optional[str] = None

    class Config:
        orm_mode = True

# Project schemas


class ResearcherProjectUpdate(BaseModel):
    commission_file_id: int


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
    creator_id: int
    created_at: datetime

    state: str
    start_at: date
    end_at: date
    title: str
    master: Optional[MasterResponse] = None
    price: Optional[str] = None
    proposal: ProposalResponse
    supervisor: UserInfoLimitedResponse
    # researcher: UserInfoLimitedResponse
    user: UserInfoLimitedResponse

    class Config:
        from_attributes = True


# Report schemas
class ReportRequest(BaseModel):
    title: str
    project_id: int
    comment: str
    file_pdf_id: int
    file_docx_id: int
    file_pptx_id: int
    anounced_percent: int

    # state: int


class ReportResponse(BaseModel):
    id: int
    creator_id: int
    created_at: datetime

    title: str

    comment: str
    state: str
    anounced_percent: int
    accepted_percent: Optional[int] = None
    project_id: int
    file_pdf_id: int
    file_docx_id: int
    file_pptx_id: int
    supervisor_file_id: int
    project: ProjectResponse

    class Config:
        from_attributes = True


class ReportUpdate(BaseModel):
    #    state: str
    comment: str
    accepted_percent: int
    commission_date_time: Optional[datetime] = None


# log

class LogResponse(BaseModel):
    id: int
    user_name: Optional[str] = None
    act: Optional[str] = None
    created_at: Optional[datetime] = None

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

from doctest import master
from sre_parse import State
import enum
from sqlalchemy import Boolean, Column, Enum, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class AllocatetState(enum.Enum):
    pending_to_specify_title = "اجرا جهت تعیین موضوع"
    pending_to_specify_master = "در انتظار انتخاب استاد راهنما"
    pending_to_accept = "در انتطار تایید"
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


class UserRole(Base):
    __tablename__ = "user_role"
    id = Column(Integer, primary_key=True)
    title = Column(String(999))


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    user_type_id = Column(Integer, ForeignKey("user_role.id"))
    fname = Column(String(999))
    lname = Column(String(999))
    father_name = Column(String(999))
    birth = Column(Date)

    resume_file_id = Column(Integer, ForeignKey("file.id"))
    address = Column(String(999))
    username = Column(String(999))
    password = Column(String(999))
    phone = Column(String(999))
    active = Column(Boolean)


class RFPField(Base):
    __tablename__ = "RFP_field"
    id = Column(Integer, primary_key=True)
    title = Column(String(999))


class RFP(Base):
    __tablename__ = "RFP"
    id = Column(Integer, primary_key=True)
    info = Column(String(999))
    creator_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime)

    file_id = Column(Integer, ForeignKey("file.id"))
    RFP_field_id = Column(Integer, ForeignKey("RFP_field.id"))

    RFP_field = relationship("RFPField", foreign_keys=[RFP_field_id])
    creator = relationship("User", foreign_keys=[creator_id])


class Allocate(Base):
    __tablename__ = "allocate"
    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime)

    RFP_id = Column(Integer, ForeignKey("RFP.id"))
    allocated_to_user_id = Column(Integer, ForeignKey("user.id"))
    project_title = Column(String(999), nullable=True)
    project_description = Column(String(999), nullable=True)
    state = Column(Enum(AllocatetState))
    # supervisor_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    master = Column(String(999), nullable=True)

    rfp = relationship("RFP", foreign_keys=[RFP_id])
    allocated_to_user = relationship(
        "User", foreign_keys=[allocated_to_user_id]
    )
    # supervisor = relationship("User", foreign_keys=[supervisor_id])
    creator = relationship("User", foreign_keys=[creator_id])


class File(Base):
    __tablename__ = "file"
    id = Column(Integer, primary_key=True)
    # creator_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime)

    info = Column(String(999))


class Proposal(Base):
    __tablename__ = "proposal"
    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime)
    master_name_and_family = Column(String(999), nullable=True)
    title = Column(String(999))
    description = Column(String(999))
    RFP_id = Column(Integer, ForeignKey("RFP.id"))
    allocate_id = Column(Integer, ForeignKey("allocate.id"))
    start_at = Column(Date, nullable=True)
    end_at = Column(Date, nullable=True)

    supervisor_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    file_id = Column(Integer, ForeignKey("file.id"), nullable=True)
    state = Column(Enum(ProposalState))  # ENUM
    comment = Column(String(999))

    rfp = relationship("RFP", foreign_keys=[RFP_id])
    user = relationship("User", foreign_keys=[user_id])
    supervisor = relationship("User", foreign_keys=[supervisor_id])
    creator = relationship("User", foreign_keys=[creator_id])


class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime)

    start_at = Column(Date)
    end_at = Column(Date)
    title = Column(String(999))
    master = Column(String(999))
    proposal_id = Column(Integer, ForeignKey("proposal.id"))
    user_supervisor_id = Column(Integer, ForeignKey("user.id"))
    # user_researcher_id = Column(Integer, ForeignKey("user.id"))
    user_user_id = Column(Integer, ForeignKey("user.id"))

    accepted_percent = Column(Integer)
    state = Column(Enum(ProjectState))

    proposal = relationship("Proposal", foreign_keys=[proposal_id])
    supervisor = relationship("User", foreign_keys=[user_supervisor_id])
    # researcher = relationship("User", foreign_keys=[user_researcher_id])
    user = relationship("User", foreign_keys=[user_user_id])
    creator = relationship("User", foreign_keys=[creator_id])


class Notification(Base):
    __tablename__ = "notification"
    id = Column(Integer, primary_key=True)
    owner = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime)
    title = Column(String(999))
    seen = Column(Boolean)
    # description = Column(String(999))


class Report(Base):
    __tablename__ = "report"
    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime)

    title = Column(String(999))

    comment = Column(String(999))
    state = Column(Enum(ReportState))  # ENUM
    anounced_percent = Column(Integer)
    accepted_percent = Column(Integer, nullable=True)
    project_id = Column(Integer, ForeignKey("project.id"))
    file_pdf_id = Column(Integer, ForeignKey("file.id"))
    file_docx_id = Column(Integer, ForeignKey("file.id"))
    file_pptx_id = Column(Integer, ForeignKey("file.id"))

    project = relationship("Project", foreign_keys=[project_id])
    creator = relationship("User", foreign_keys=[creator_id])


class Master(Base):
    __tablename__ = "masterr"
    id = Column(Integer, primary_key=True)
    name = Column(String(999))

# class ReportFile(Base):
#     __tablename__ = "report_file"
#     id = Column(Integer, primary_key=True)
#     info = Column(String(999))
#     report_id = Column(Integer, ForeignKey("report.id"))
#     file_id = Column(Integer, ForeignKey("file.id"))

#     report = relationship("Report", foreign_keys=[report_id])

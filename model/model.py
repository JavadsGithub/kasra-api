from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


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


class RFP(Base):
    __tablename__ = "RFP_main"
    id = Column(Integer, primary_key=True)
    info = Column(String(999))
    file_id = Column(Integer, ForeignKey("file.id"))
    RFP_field_id = Column(Integer, ForeignKey("RFP_field.id"))


class RFPField(Base):
    __tablename__ = "RFP_field"
    id = Column(Integer, primary_key=True)
    title = Column(String(999))


class File(Base):
    __tablename__ = "file"
    id = Column(Integer, primary_key=True)
    info = Column(String(999))
    access_id = Column(Integer, ForeignKey("user_role.id"))
    # access = relationship("UserRole")


class Proposal(Base):
    __tablename__ = "proposal"
    id = Column(Integer, primary_key=True)
    info = Column(String(999))
    RFP_id = Column(Integer, ForeignKey("RFP_main.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    file_id = Column(Integer, ForeignKey("file.id"))
    state = Column(Integer)  # ENUM
    comment = Column(String(999))

    # rfp = relationship("RFP", back_populates="proposals")
    # user = relationship("User")
    # file = relationship("File")


class Commission(Base):
    __tablename__ = "commission"
    id = Column(Integer, primary_key=True)
    title = Column(String(999))
    comment = Column(String(999))
    state = Column(Integer)  # ENUM
    proposal_id = Column(Integer, ForeignKey("proposal.id"))
    user_supervisor_id = Column(Integer, ForeignKey("user.id"))
    user_discoverer_id = Column(Integer, ForeignKey("user.id"))
    file_id = Column(Integer, ForeignKey("file.id"))

    # proposal = relationship("Proposal")
    # supervisor = relationship("User", foreign_keys=[user_supervisor_id])
    # discoverer = relationship("User", foreign_keys=[user_discoverer_id])


class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    title = Column(String(999))
    proposal_id = Column(Integer, ForeignKey("proposal.id"))
    user_supervisor_id = Column(Integer, ForeignKey("user.id"))
    user_discoverer_id = Column(Integer, ForeignKey("user.id"))
    user_master_id = Column(Integer, ForeignKey("user.id"))
    user_broker_id = Column(Integer, ForeignKey("user.id"))
    user_user_id = Column(Integer, ForeignKey("user.id"))

    # proposal = relationship("Proposal")
    # supervisor = relationship("User", foreign_keys=[user_supervisor_id])
    # discoverer = relationship("User", foreign_keys=[user_discoverer_id])
    # master = relationship("User", foreign_keys=[user_master_id])
    # broker = relationship("User", foreign_keys=[user_broker_id])
    # user = relationship("User", foreign_keys=[user_user_id])


class Report(Base):
    __tablename__ = "report"
    id = Column(Integer, primary_key=True)
    info = Column(String(999))
    project_id = Column(Integer, ForeignKey("project.id"))
    comment = Column(String(999))
    state = Column(Integer)  # ENUM

    # project = relationship("Project")
    # report_files = relationship("ReportFile", back_populates="report")


class ReportFile(Base):
    __tablename__ = "report_file"
    id = Column(Integer, primary_key=True)
    info = Column(String(999))
    report_id = Column(Integer, ForeignKey("report.id"))
    file_id = Column(Integer, ForeignKey("file.id"))

    # report = relationship("Report", back_populates="report_files")

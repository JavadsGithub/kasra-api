from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session

import datetime
from service.user import reports_exist
from repository.user import *
from util.util import *
from util import util
from model import database, model

router = APIRouter(tags=["seed"], prefix="/seed")


@router.get("/seed/")
async def add_proposal(db: Session = Depends(get_db)):

    db.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
    result = db.execute(text("SHOW TABLES;"))
    tables = [row[0] for row in result.fetchall()]
    for table in tables:
        db.execute(text(f"DROP TABLE IF EXISTS {table};"))

    model.Base.metadata.create_all(database.engine)

    new_user_roules = [
        UserRole(title="کارگزار"),  # 1
        UserRole(title="کاشف"),  # 2
        UserRole(title="کارجو"),  # 3
        UserRole(title="ناظر"),  # 4
        UserRole(title="امور محققین"),  # 5
        UserRole(title="admin"),  # 6
    ]
    db.add_all(new_user_roules)
    db.commit()

    rolese = db.query(UserRole).all()
    new_file = File(info="file.pdf", created_at=datetime.now(),)
    db.add(new_file)
    db.commit()
    file_id = db.query(File).first().id

    new_users = [
        User(
            user_type_id=rolese[0].id,
            fname="جواد",
            lname="جوادی",
            father_name="محمدجواد",
            resume_file_id=file_id,
            birth=datetime.now(),
            address="همدان-جوادیه",
            username="admin",
            password=util.hash("admin"),
            phone="09181020300",
            active=True,
        ),
        User(
            user_type_id=rolese[1].id,
            fname="علی",
            lname="اکبری",
            father_name="حسن",
            birth=datetime.now(),
            resume_file_id=file_id,
            address="تهران-اکبرآباد",
            username="admin2",
            password=util.hash("admin"),
            phone="09182020301",
            active=True,
        ),
        User(
            user_type_id=rolese[2].id,
            fname="سارا",
            lname="موسوی",
            father_name="محمد",
            birth=datetime.now(),
            resume_file_id=file_id,
            address="اصفهان-موسوی",
            username="admin3",
            password=util.hash("admin"),
            phone="09183020302",
            active=True,
        ),

        User(
            user_type_id=rolese[3].id,
            fname="زهرا",
            lname="حسینی",
            father_name="علی",
            birth=datetime.now(),
            resume_file_id=file_id,
            address="شیراز-حسینیه",
            username="admin4",
            password=util.hash("admin"),
            phone="09184020303",
            active=True,
        ),
        User(
            user_type_id=rolese[4].id,
            fname="رضا",
            lname="نیکو",
            father_name="سید",
            birth=datetime.now(),
            resume_file_id=file_id,
            address="مشهد-رضوی",
            username="admin5",
            password=util.hash("admin"),
            phone="09185020304",
            active=True,
        ),
        User(
            user_type_id=rolese[5].id,
            fname="محسن",
            lname="عالینژاد",
            father_name="حسن",
            birth=datetime.now(),
            resume_file_id=file_id,
            address="مشهد-رضوی",
            username="admin6",
            password=util.hash("admin"),
            phone="09185020304",
            active=True,
        ),
        # repeat
        User(
            user_type_id=rolese[2].id,
            fname="فاطمه",
            lname="عالینژاد",
            father_name="محمد",
            birth=datetime.now(),
            resume_file_id=file_id,
            address="اصفهان-موسوی",
            username="admin7",
            password=util.hash("admin"),
            phone="09183020302",
            active=True,
        ),
    ]
    db.add_all(new_users)
    db.commit()

    new_RFP_fields = [
        RFPField(title="صنعت خودرو"),
        RFPField(title="کامپیوتر و it"),
        RFPField(title="کشاورزی"),
        RFPField(title="صنایع شیمی"),
        RFPField(title="صنایع هوافضا"),
        RFPField(title="امنیت سایبری"),
        RFPField(title="هوش مصنوعی"),
        RFPField(title="علوم انسانی"),
    ]
    db.add_all(new_RFP_fields)
    db.commit()

    fieldss = db.query(RFPField).all()

    new_rfps = [
        RFP(
            info="درخواست پروژه IT و نرم‌افزار",
            file_id=file_id,
            RFP_field_id=fieldss[1].id,
            creator_id=2,
            created_at=datetime.now(),
        ),

        RFP(
            info="نیاز به تأمین مواد شیمیایی",
            file_id=file_id,
            RFP_field_id=fieldss[3].id,
            creator_id=2,
            created_at=datetime.now(),
        ),
        RFP(
            info="پروژه تحقیقاتی در صنعت هوافضا",
            file_id=file_id,
            RFP_field_id=fieldss[4].id,
            creator_id=2,
            created_at=datetime.now(),
        ),
        RFP(
            info="ایجاد زیرساخت امنیت سایبری",
            file_id=file_id,
            RFP_field_id=fieldss[5].id,
            creator_id=2,
            created_at=datetime.now(),
        ),
        RFP(
            info="تحقیق و توسعه در هوش مصنوعی",
            file_id=file_id,
            RFP_field_id=fieldss[6].id,
            creator_id=2,
            created_at=datetime.now(),
        ),
        RFP(
            info="پروژه در علوم انسانی",
            file_id=file_id, RFP_field_id=fieldss[7].id,
            creator_id=2,
            created_at=datetime.now(),
        ),

        RFP(
            info="برنامه‌ریزی برای توسعه صنعت خودرو",
            file_id=file_id,
            RFP_field_id=fieldss[7].id,
            creator_id=2,
            created_at=datetime.now(),
        ),
        RFP(
            info="توسعه نرم‌افزارهای IT",
            file_id=file_id, RFP_field_id=fieldss[1].id,
            creator_id=2,
            created_at=datetime.now(),
        ),
        RFP(
            info="بهینه‌سازی در کشاورزی",
            file_id=file_id, RFP_field_id=fieldss[2].id,
            creator_id=2,
            created_at=datetime.now(),
        ),
        RFP(
            info="تحقیقات در زمینه صنایع شیمیایی",
            file_id=file_id,
            RFP_field_id=fieldss[3].id,
            creator_id=2,
            created_at=datetime.now(),
        ),
        RFP(
            info="نوآوری در صنعت هوافضا",
            file_id=file_id, RFP_field_id=fieldss[4].id,
            creator_id=2,
            created_at=datetime.now(),
        ),
        RFP(
            info="تقویت امنیت سایبری", file_id=file_id,
            RFP_field_id=fieldss[5].id, creator_id=2,
            created_at=datetime.now(),
        ),
        RFP(
            info="ایجاد پروژه‌های هوش مصنوعی",
            file_id=file_id,
            RFP_field_id=fieldss[6].id, creator_id=2,
            created_at=datetime.now(),
        ),
    ]
    db.add_all(new_rfps)
    db.commit()
    new_masters = [
        Master(
            name="حجت مختاری"
        ),
        Master(
            name="محمد اسدی"
        ),
        Master(
            name="علی محمودی"
        ),
        Master(
            name="حسن صادقی"
        ),
    ]
    db.add_all(new_masters)
    db.commit()

    user_id = db.query(User).first().id
    RFP_id = db.query(RFP).first().id

    new_allocates = [
        Allocate(
            master_id=1,
            allocated_to_user_id=3,
            state=AllocatetState.pending_to_specify_title,
            creator_id=1,
            created_at=datetime.now(),
            project_title="",
            project_description="",
            RFP_id=RFP_id,
        ),
        Allocate(
            master_id=1,
            allocated_to_user_id=3,
            state=AllocatetState.rejected,
            creator_id=1,
            created_at=datetime.now(),
            project_title="project1",
            project_description="",
            RFP_id=RFP_id,
        ),
        Allocate(
            master_id=1,
            allocated_to_user_id=3,
            state=AllocatetState.eccepted,
            creator_id=1,
            created_at=datetime.now(),
            project_title="project1",
            project_description="",
            RFP_id=RFP_id,
        ),
        Allocate(
            master_id=1,
            allocated_to_user_id=3,
            state=AllocatetState.pending_to_specify_master,
            creator_id=1,
            created_at=datetime.now(),
            project_title="project1",
            project_description="",
            RFP_id=RFP_id,
        ),
        Allocate(
            master_id=1,
            allocated_to_user_id=3,
            state=AllocatetState.pending_to_accept,
            creator_id=1,
            created_at=datetime.now(),
            project_title="project1",
            project_description="",
            RFP_id=RFP_id,
        )
    ]
    db.add_all(new_allocates)
    db.commit()
    new_proposal = [
        Proposal(
            supervisor_id=4,
            user_id=3,
            file_id=file_id,
            state=ProposalState.eccepted,
            comment="",
            creator_id=2,
            created_at=datetime.now(),
            master_id=1,
            title="پروپوزال1 ",
            description="",
            RFP_id=RFP_id,
            allocate_id=1,
            start_at=datetime.now(),
            end_at=datetime.now(),
        ),
        Proposal(
            supervisor_id=4,
            user_id=3,
            file_id=file_id,
            state=ProposalState.pending_to_accept,
            comment="",
            creator_id=2,
            created_at=datetime.now(),
            master_id=1,
            title="پروپوزال2 ",
            description="",
            RFP_id=RFP_id,
            allocate_id=1,
            start_at=datetime.now(),
            end_at=datetime.now(),
        ),
        Proposal(
            supervisor_id=4,
            user_id=3,
            file_id=file_id,
            state=ProposalState.pending_to_explorer_accept,
            comment="",
            creator_id=2,
            created_at=datetime.now(),
            master_id=1,
            title="",
            description="",
            RFP_id=RFP_id,
            allocate_id=1,
            start_at=datetime.now(),
            end_at=datetime.now(),
        ),
        Proposal(
            supervisor_id=4,
            user_id=3,
            file_id=file_id,
            state=ProposalState.rejected,
            comment="",
            creator_id=2,
            created_at=datetime.now(),
            master_id=1,
            title="پروپوزال4",
            description="",
            RFP_id=RFP_id,
            allocate_id=1,
            start_at=datetime.now(),
            end_at=datetime.now(),
        )
    ]
    db.add_all(new_proposal)
    db.commit()

    proposals = db.query(Proposal).all()

    users_for_roles = [
        db.query(User).filter(User.user_type_id == rolese[0].id).first(),
        db.query(User).filter(User.user_type_id == rolese[1].id).first(),
        db.query(User).filter(User.user_type_id == rolese[2].id).first(),
        db.query(User).filter(User.user_type_id == rolese[3].id).first(),
        db.query(User).filter(User.user_type_id == rolese[4].id).first(),
    ]

    new_projects = [
        Project(
            user_supervisor_id=4,
            user_user_id=3,
            state=ProjectState.active,

            creator_id=2,
            created_at=datetime.now(),
            master_id=1,
            title="project 1",
            proposal_id=proposals[0].id,
            start_at=datetime.now(),
            end_at=datetime.now(),
            accepted_percent=10,
        ),
        Project(
            user_supervisor_id=4,
            user_user_id=3,
            state=ProjectState.active,
            creator_id=2,
            created_at=datetime.now(),
            master_id=1,
            title="project 2",
            proposal_id=proposals[1].id,
            start_at=datetime.now(),
            end_at=datetime.now(),
            accepted_percent=60,
        ),
        Project(
            user_supervisor_id=4,
            user_user_id=3,
            state=ProjectState.active,
            creator_id=2,
            created_at=datetime.now(),
            master_id=1,
            title="project 3",
            proposal_id=proposals[2].id,
            start_at=datetime.now(),
            end_at=datetime.now(),
            accepted_percent=100,
        ),
    ]

    db.add_all(new_projects)
    db.commit()
    project_id = db.query(Project).first().id
    new_reports = [
        Report(
            creator_id=3,
            created_at=datetime.now(),
            title="report 1",
            project_id=project_id,
            comment="none",
            state=ReportState.eccepted,
            file_pdf_id=file_id,
            file_docx_id=file_id,
            file_pptx_id=file_id,
            anounced_percent=20,
            accepted_percent=10,
        ),
        Report(
            creator_id=3,
            created_at=datetime.now(),
            title="report 2",
            project_id=project_id,
            comment="none",
            state=ReportState.pending,
            file_pdf_id=file_id,
            file_docx_id=file_id,
            file_pptx_id=file_id,
            anounced_percent=70,
            accepted_percent=0,
        ),
        Report(
            creator_id=3,
            created_at=datetime.now(),
            title="report 3",
            project_id=project_id,
            comment="none",
            state=ReportState.rejected,
            file_pdf_id=file_id,
            file_docx_id=file_id,
            file_pptx_id=file_id,
            anounced_percent=70,
            accepted_percent=0,
        ),
        Report(
            creator_id=3,
            created_at=datetime.now(),
            title="report 4",
            project_id=project_id,
            comment="none",
            state=ReportState.eccepted,
            file_pdf_id=file_id,
            file_docx_id=file_id,
            file_pptx_id=file_id,
            anounced_percent=100,
            accepted_percent=100,
        ),
    ]
    db.add_all(new_reports)
    db.commit()

    # report_id = db.query(Report).first().id
    # new_report_files = [
    #     ReportFile(
    #         info="file 1",
    #         report_id=report_id,
    #         file_id=file_id,
    #     ),
    #     ReportFile(
    #         info="file 2",
    #         report_id=report_id,
    #         file_id=file_id,
    #     ),
    # ]
    # db.add_all(new_report_files)
    # db.commit()

    return {"response": "ok"}

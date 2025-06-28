from util.util import *
from sqlalchemy.orm import Session
from model.model import *
import datetime
from util import util


def seeding():
    db = database.SessionLocal()

    

    new_user_roules = [
        UserRole(title="کارگزار"),
        UserRole(title="کاشف"),
        UserRole(title="کاربر"),
        UserRole(title="ناظر"),
        UserRole(title="استاد راهنما"),
    ]
    db.add_all(new_user_roules)
    db.commit()
    new_file = File(info="file.pdf", access_id=1)
    db.add(new_file)
    db.commit()
    
    rolese = db.query(UserRole).all()

    new_users = [
        User(
            user_type_id=rolese[0].id,
            fname="جواد",
            lname="جوادی",
            father_name="محمدجواد",
            resume_file_id=1,
            birth=datetime.datetime.now(),
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
            birth=datetime.datetime.now(),
            resume_file_id=28,
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
            birth=datetime.datetime.now(),
            resume_file_id=1,
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
            birth=datetime.datetime.now(),
            resume_file_id=1,
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
            birth=datetime.datetime.now(),
            resume_file_id=1,
            address="مشهد-رضوی",
            username="admin5",
            password=util.hash("admin"),
            phone="09185020304",
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
        RFP(info="درخواست پروژه IT و نرم‌افزار", file_id=1, RFP_field_id=fieldss[1].id),
        # RFP(info="طرح برای بهبود کشاورزی", file_id=1, RFP_field_id=fieldss[2].id),
        # RFP(info="نیاز به تأمین مواد شیمیایی", file_id=1, RFP_field_id=fieldss[3].id),
        # RFP(info="پروژه تحقیقاتی در صنعت هوافضا", file_id=1, RFP_field_id=fieldss[4].id),
        # RFP(info="ایجاد زیرساخت امنیت سایبری", file_id=1, RFP_field_id=fieldss[5].id),
        # RFP(info="تحقیق و توسعه در هوش مصنوعی", file_id=1, RFP_field_id=fieldss[6].id),
        # RFP(info="پروژه در علوم انسانی", file_id=1, RFP_field_id=fieldss[7].id),
        # RFP(info="برنامه‌ریزی برای توسعه صنعت خودرو", file_id=2, RFP_field_id=fieldss[7].id),
        # RFP(info="توسعه نرم‌افزارهای IT", file_id=1, RFP_field_id=fieldss[1].id),
        # RFP(info="بهینه‌سازی در کشاورزی", file_id=1, RFP_field_id=fieldss[2].id),
        # RFP(info="تحقیقات در زمینه صنایع شیمیایی", file_id=2, RFP_field_id=fieldss[3].id),
        # RFP(info="نوآوری در صنعت هوافضا", file_id=1, RFP_field_id=fieldss[4].id),
        # RFP(info="تقویت امنیت سایبری", file_id=1, RFP_field_id=fieldss[5].id),
        # RFP(info="ایجاد پروژه‌های هوش مصنوعی", file_id=1, RFP_field_id=fieldss[6].id),
    ]
    db.add_all(new_rfps)
    db.commit()

    new_proposal = [
        Proposal(
            info="پروپوزال۱ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""
        ),
        Proposal(
            info="پروپوزال۲ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""
        ),
        Proposal(
            info="پروپوزال۳ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""
        ),
        Proposal(
            info="پروپوزال۴ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""
        ),
        Proposal(
            info="پروپوزال۵ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""
        ),
        Proposal(
            info="پروپوزال۶ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""
        ),
        Proposal(
            info="پروپوزال۷ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""
        ),
        Proposal(
            info="پروپوزال۸ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""
        ),
        Proposal(
            info="پروپوزال۹ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""
        ),
        Proposal(
            info="پروپوزال۱۰ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""
        ),
        Proposal(
            info="پروپوزال۱۱ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""
        ),
        Proposal(
            info="پروپوزال۱۲ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""
        ),
        Proposal(
            info="پروپوزال۱۳ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""
        ),
    ]
    db.add_all(new_proposal)
    db.commit()

    new_projects = [
        Project(
            title="project 1",
            proposal_id=1,
            user_supervisor_id=4,
            user_discoverer_id=2,
            user_master_id=1,
            user_broker_id=1,
            user_user_id=3,
        ),
        Project(
            title="project 2",
            proposal_id=1,
            user_supervisor_id=4,
            user_discoverer_id=2,
            user_master_id=1,
            user_broker_id=1,
            user_user_id=3,
        ),
        Project(
            title="project 3",
            proposal_id=1,
            user_supervisor_id=4,
            user_discoverer_id=2,
            user_master_id=1,
            user_broker_id=1,
            user_user_id=3,
        ),
        Project(
            title="project 4",
            proposal_id=1,
            user_supervisor_id=4,
            user_discoverer_id=2,
            user_master_id=1,
            user_broker_id=1,
            user_user_id=3,
        ),
        Project(
            title="project 5",
            proposal_id=1,
            user_supervisor_id=4,
            user_discoverer_id=2,
            user_master_id=1,
            user_broker_id=1,
            user_user_id=3,
        ),
        Project(
            title="project 6",
            proposal_id=1,
            user_supervisor_id=4,
            user_discoverer_id=2,
            user_master_id=1,
            user_broker_id=1,
            user_user_id=3,
        ),
        Project(
            title="project 7",
            proposal_id=1,
            user_supervisor_id=4,
            user_discoverer_id=2,
            user_master_id=1,
            user_broker_id=1,
            user_user_id=3,
        ),
        Project(
            title="project 8",
            proposal_id=1,
            user_supervisor_id=4,
            user_discoverer_id=2,
            user_master_id=1,
            user_broker_id=1,
            user_user_id=3,
        ),
        Project(
            title="project 9",
            proposal_id=1,
            user_supervisor_id=4,
            user_discoverer_id=2,
            user_master_id=1,
            user_broker_id=1,
            user_user_id=3,
        ),
        Project(
            title="project 10",
            proposal_id=1,
            user_supervisor_id=4,
            user_discoverer_id=2,
            user_master_id=1,
            user_broker_id=1,
            user_user_id=3,
        ),
        Project(
            title="project 11",
            proposal_id=1,
            user_supervisor_id=4,
            user_discoverer_id=2,
            user_master_id=1,
            user_broker_id=1,
            user_user_id=3,
        ),
        Project(
            title="project 12",
            proposal_id=1,
            user_supervisor_id=4,
            user_discoverer_id=2,
            user_master_id=1,
            user_broker_id=1,
            user_user_id=3,
        ),
        Project(
            title="project 13",
            proposal_id=1,
            user_supervisor_id=4,
            user_discoverer_id=2,
            user_master_id=1,
            user_broker_id=1,
            user_user_id=3,
        ),
        Project(
            title="project 14",
            proposal_id=1,
            user_supervisor_id=4,
            user_discoverer_id=2,
            user_master_id=1,
            user_broker_id=1,
            user_user_id=3,
        ),
        Project(
            title="project 15",
            proposal_id=1,
            user_supervisor_id=4,
            user_discoverer_id=2,
            user_master_id=1,
            user_broker_id=1,
            user_user_id=3,
        ),
    ]
    db.add_all(new_projects)
    db.commit()

    new_reports = [
        Report(
            info="report 1",
            project_id=1,
            comment="none",
            state=1,
        ),
        Report(
            info="report 2",
            project_id=1,
            comment="none",
            state=2,
        ),
        Report(
            info="report 2",
            project_id=1,
            comment="none",
            state=3,
        ),
    ]
    db.add_all(new_reports)

    new_report_files = [
        ReportFile(
            info="file 1",
            report_id=1,
            file_id=1,
        ),
        ReportFile(
            info="file 2",
            report_id=1,
            file_id=1,
        ),
    ]
    db.add_all(new_report_files)
    db.commit()

    db.commit()

from util.util import *
from sqlalchemy.orm import Session
from model.model import *
from time import datetime
from util import util

db: Session = get_db()

new_file = File(info="file.pdf")
db.add(new_file)

new_user_roules = [
    UserRole(title="کارگزار"),
    UserRole(title="کاشف"),
    UserRole(title="کاربر"),
    UserRole(title="ناظر"),
    UserRole(title="استاد راهنما"),
]
db.add_all(new_user_roules)

new_users = [
    User(
        user_type_id=1,
        fname="جواد",
        lname="جوادی",
        father_name="محمدجواد",
        resume_file_id=1,
        birth=datetime.datetime.now(),
        address="همدان-جوادیه",
        username="admin1",
        password=util.hash("admin"),
        phone="09181020300",
        active=True,
    ),
    User(
        user_type_id=2,
        fname="علی",
        lname="اکبری",
        father_name="حسن",
        birth=datetime.datetime.now(),
        resume_file_id=1,
        address="تهران-اکبرآباد",
        username="admin2",
        password=util.hash("admin"),
        phone="09182020301",
        active=True,
    ),
    User(
        user_type_id=3,
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
        user_type_id=4,
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
        user_type_id=5,
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

new_rfps = [
    RFP(info="نیاز به مشاوره هوش مصنوعی در صنعت خودرو", file_id=1, field_id=1),
    RFP(info="درخواست پروژه IT و نرم‌افزار", file_id=1, field_id=2),
    RFP(info="طرح برای بهبود کشاورزی", file_id=1, field_id=3),
    RFP(info="نیاز به تأمین مواد شیمیایی", file_id=1, field_id=4),
    RFP(info="پروژه تحقیقاتی در صنعت هوافضا", file_id=1, field_id=5),
    RFP(info="ایجاد زیرساخت امنیت سایبری", file_id=1, field_id=6),
    RFP(info="تحقیق و توسعه در هوش مصنوعی", file_id=1, field_id=7),
    RFP(info="پروژه در علوم انسانی", file_id=1, field_id=8),
    RFP(info="برنامه‌ریزی برای توسعه صنعت خودرو", file_id=2, field_id=1),
    RFP(info="توسعه نرم‌افزارهای IT", file_id=1, field_id=2),
    RFP(info="بهینه‌سازی در کشاورزی", file_id=1, field_id=3),
    RFP(info="تحقیقات در زمینه صنایع شیمیایی", file_id=2, field_id=4),
    RFP(info="نوآوری در صنعت هوافضا", file_id=1, field_id=5),
    RFP(info="تقویت امنیت سایبری", file_id=1, field_id=6),
    RFP(info="ایجاد پروژه‌های هوش مصنوعی", file_id=1, field_id=7),
]
db.add_all(new_rfps)

new_proposal = [
    Proposal(info="پروپوزال۱ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""),
    Proposal(info="پروپوزال۲ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""),
    Proposal(info="پروپوزال۳ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""),
    Proposal(info="پروپوزال۴ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""),
    Proposal(info="پروپوزال۵ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""),
    Proposal(info="پروپوزال۶ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""),
    Proposal(info="پروپوزال۷ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""),
    Proposal(info="پروپوزال۸ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""),
    Proposal(info="پروپوزال۹ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""),
    Proposal(info="پروپوزال۱۰ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""),
    Proposal(info="پروپوزال۱۱ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""),
    Proposal(info="پروپوزال۱۲ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""),
    Proposal(info="پروپوزال۱۳ ", RFP_id=1, user_id=1, file_id=1, state=1, comment=""),
]
db.add_all(new_proposal)


db.add_all(new_user_roules)
db.add_all(new_users)
db.commit()

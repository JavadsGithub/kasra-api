from sqlalchemy.orm import Session
from model import schemas
from model.model import RFP, RFPField
from model.schemas import *
from fastapi import HTTPException
from datetime import datetime


def explorer_search_rfps(db: Session, skip: int = 0, limit: int = 10, info: str = None):
    query = db.query(RFP).order_by(RFP.id.desc())
    if info:
        query = query.filter(RFP.info.ilike(f"%{info}%"))
    return query.offset(skip).limit(limit).all()


def user_search_rfps(db: Session, skip: int = 0, limit: int = 10, info: str = None):
    query = db.query(RFP).order_by(RFP.id.desc())
    if info:
        query = query.filter(RFP.info.ilike(f"%{info}%"))
    return query.offset(skip).limit(limit).all()


def explorer_rfp_single(db: Session, rfp_id: int):
    return db.query(RFP).filter(RFP.id == rfp_id).first()


def explorer_get_rfps(db: Session, skip: int = 0, limit: int = 10):
    return db.query(RFP).order_by(RFP.id.desc()).offset(skip).limit(limit).all()


def explorer_get_rfp_fields(db: Session, skip: int = 0, limit: int = 10):
    return db.query(RFPField).offset(skip).limit(limit).all()


def explorer_create_rfp(db: Session, rfp: ExplorerCreateUpdateRFP, creator_id: int):
    new_rfp = RFP(
        info=rfp.info,
        RFP_field_id=rfp.RFP_field_id,
        file_id=rfp.file_id,
        creator_id=creator_id,
        created_at=datetime.now(),
        beneficiary=rfp.beneficiary,  # کاربر بهره‌بردار
        representative=rfp.representative,  # نماینده بهره‌بردار
        issue_title=rfp.issue_title,  # عنوان مسئله
        issue_description=rfp.issue_description,  # شرح مختصر مسئله
        mission_area=rfp.mission_area,  # حوضه ماموریتی
        specialty_field=rfp.specialty_field,  # رشته و گرایش تخصصی
        issue_origin=rfp.issue_origin,  # توضیحات درباره منشا یافتن مسئله
        proposed_execution_path=rfp.proposed_execution_path,  # توضیحات مسیر پیشنهادی اجرا
        frequency=rfp.frequency,  # فراوانی
        financial_value=rfp.financial_value,  # ارزش مالی مسئله
        key_requirements=rfp.key_requirements,  # الزامات کلیدی و حیاتی
        limitations=rfp.limitations,  # محدودیت ها
        technical_solution=rfp.technical_solution,  # راه حل فنی
        related_projects=rfp.related_projects,  # پروژه های مرتبط
        proposed_product=rfp.proposed_product,  # محصول پیشنهادی
        issue_support=rfp.issue_support,  # نحوه حمایت از مسئله
        analyst_evaluator=rfp.analyst_evaluator,  # تحلیل کارگزار کاشف
        keywords=rfp.keywords  # کلمات کلیدی
    )
    rfp_exists = db.query(RFP).filter(RFP.info == rfp.info).all()
    if rfp_exists:
        raise HTTPException(status_code=403, detail="RFP already exists")
    db.add(new_rfp)
    db.commit()
    db.refresh(new_rfp)
    return new_rfp


def explorer_update_rfp(db: Session, rfp_id: int, rfp_update: ExplorerCreateUpdateRFP):
    rfp = db.query(RFP).filter(RFP.id == rfp_id).first()
    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")
    if rfp_update.info is not None:
        rfp.info = rfp_update.info
    if rfp_update.file_id is not None:
        rfp.file_id = rfp_update.file_id
    if rfp_update.RFP_field_id is not None:
        rfp.RFP_field_id = rfp_update.RFP_field_id

    if rfp_update.beneficiary is not None:
        rfp.beneficiary = rfp_update.beneficiary  # کاربر بهره‌بردار
    if rfp_update.representative is not None:
        rfp.representative = rfp_update.representative  # نماینده بهره‌بردار
    if rfp_update.issue_title is not None:
        rfp.issue_title = rfp_update.issue_title  # عنوان مسئله
    if rfp_update.issue_description is not None:
        rfp.issue_description = rfp_update.issue_description  # شرح مختصر مسئله
    if rfp_update.mission_area is not None:
        rfp.mission_area = rfp_update.mission_area  # حوضه ماموریتی
    if rfp_update.specialty_field is not None:
        rfp.specialty_field = rfp_update.specialty_field  # رشته و گرایش تخصصی
    if rfp_update.issue_origin is not None:
        rfp.issue_origin = rfp_update.issue_origin  # توضیحات درباره منشا یافتن مسئله
    if rfp_update.proposed_execution_path is not None:
        # توضیحات مسیر پیشنهادی اجرا
        rfp.proposed_execution_path = rfp_update.proposed_execution_path
    if rfp_update.frequency is not None:
        rfp.frequency = rfp_update.frequency  # فراوانی
    if rfp_update.financial_value is not None:
        rfp.financial_value = rfp_update.financial_value  # ارزش مالی مسئله
    if rfp_update.key_requirements is not None:
        rfp.key_requirements = rfp_update.key_requirements  # الزامات کلیدی و حیاتی
    if rfp_update.limitations is not None:
        rfp.limitations = rfp_update.limitations  # محدودیت ها
    if rfp_update.technical_solution is not None:
        rfp.technical_solution = rfp_update.technical_solution  # راه حل فنی
    if rfp_update.related_projects is not None:
        rfp.related_projects = rfp_update.related_projects  # پروژه های مرتبط
    if rfp_update.proposed_product is not None:
        rfp.proposed_product = rfp_update.proposed_product  # محصول پیشنهادی
    if rfp_update.issue_support is not None:
        rfp.issue_support = rfp_update.issue_support  # نحوه حمایت از مسئله
    if rfp_update.analyst_evaluator is not None:
        rfp.analyst_evaluator = rfp_update.analyst_evaluator  # تحلیل کارگزار کاشف
    if rfp_update.keywords is not None:
        rfp.keywords = rfp_update.keywords  # کلمات کلیدی
    db.commit()
    db.refresh(rfp)
    return rfp


def broker_get_rfp_by_id(db: Session, rfp_id: int):
    return db.query(RFP).filter(RFP.id == rfp_id).first()

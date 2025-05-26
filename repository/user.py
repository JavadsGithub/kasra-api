from sqlalchemy.sql import exists
from sqlalchemy.orm import Session
from model import model


def user_exist(db: Session, user: model.User):
    return db.query(
        model.User.query.filter(model.User.user_name == user.user_name).exists()
    ).scalar()


def add_user(db: Session, new_user: model.User):
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

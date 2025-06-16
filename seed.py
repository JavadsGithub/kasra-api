from util.util import *
from sqlalchemy.orm import Session
from model.model import User
from time import datetime

db: Session = get_db()

new_user = User(
    user_type_id=1,
    fname="جواد",
    lname="جوادی",
    father_name="محمدجواد",
    birth=datetime.datetime.now(),
    address="همدان-جوادیه",
    username="admin",
    password="admin",
    phone="09181020300",
    active=True,
)

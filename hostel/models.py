from . import db
from . import hostellite_db
from . import mess_db
from . import message_db
from . import info_db
from . import infow_db
from .import fee_db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(40))
    hostel = db.Column(db.String(60))


class hostellite(hostellite_db.Model, UserMixin):
    id = hostellite_db.Column(db.Integer,primary_key = True)
    username = hostellite_db.Column(db.String(50))
    hostel = hostellite_db.Column(db.String(60))
    room = hostellite_db.Column(db.String(60))
    floor = hostellite_db.Column(db.String(60))

class mess(mess_db.Model , UserMixin):
    id = mess_db.Column(mess_db.Integer,primary_key = True)
    food = mess_db.Column(mess_db.String(90))
    type = mess_db.Column(mess_db.String(60))
    day = mess_db.Column(mess_db.String(50))
    
class message(message_db.Model , UserMixin):
    id = message_db.Column(message_db.Integer,primary_key = True)
    username = message_db.Column(message_db.String(60))
    subject = message_db.Column(message_db.String(120))
    info = message_db.Column(message_db.String(200))

class info(info_db.Model,UserMixin):
    id = info_db.Column(info_db.Integer,primary_key = True)
    name = info_db.Column(info_db.String(50))
    college = info_db.Column(info_db.String(50))
    stream = info_db.Column(info_db.String(10))
    phone= info_db.Column(info_db.String(15))

class infow(infow_db.Model,UserMixin):
    id = infow_db.Column(infow_db.Integer,primary_key = True)
    name = infow_db.Column(infow_db.String(50))
    phone = info_db.Column(infow_db.String(15))
    add = infow_db.Column(info_db.String(120))

class fee(fee_db.Model,UserMixin):
    id = fee_db.Column(fee_db.Integer,primary_key = True)
    name = fee_db.Column(fee_db.String(60))
    room = fee_db.Column(fee_db.String(60))
    phone = fee_db.Column(fee_db.String(60))
    hostel = fee_db.Column(fee_db.String(60))
    file = fee_db.Column(fee_db.String(1000))
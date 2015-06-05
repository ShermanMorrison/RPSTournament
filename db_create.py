__author__ = 'jonathan'

from app import db
from app.models import User

db.reflect()
db.drop_all()
db.create_all()

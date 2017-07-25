'''

User functions

'''

from models import Users
from flask import session

def get_logged_in_user(field):

	user_id = sesssion['user_id']

	user = Users.query.filter(Users.user_id == user_id).first()

	return user.field
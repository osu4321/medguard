'''

User functions

'''

from models import Users
from flask import session
from controller import get_role_name, get_user_role

def get_logged_in_user(field):

	user_id = session['user_id']

	user = Users.query.filter(Users.user_id == user_id).first()

	return getattr(user, field)




def get_logged_in_user_all():

	user_id = session['user_id']

	user = Users.query.filter(Users.user_id == user_id).first()

	user_dict = {}

	user_dict['full_name'] = getattr(user, 'first_name') + " " + getattr(user, 'last_name')
	user_dict['role_name'] = get_role_name(get_user_role(user_id))

	return user_dict



def logged_in_user_all():
	
	if session['logged_in'] == True:
		return get_logged_in_user_all()

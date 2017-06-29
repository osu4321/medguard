###########
# Controller
##########

from models import Users
from models import User_level


def get_user_role(user_id):

	user = Users.query.filter_by(user_id=user_id).first()

	if user is not None:

		return 1

		# TODO not liking backref.
		#return user.role.role_id

	else:

		return False

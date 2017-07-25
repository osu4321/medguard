###########
# Controller
##########

from models import Users, User_level, Roles
from forms import AddLibraryItemForm


ACCESS_LEVELS = {
	"doctor": 1,
	"patient": 2
}


def get_user_role(user_id):

	user = User_level.query.filter_by(user_id=user_id).first()

	if user is not None:

		return user.role_id

	else:

		return False


def get_role_name(role_id):

	role = Roles.query.filter_by(role_id=role_id).first()

	return role.name


def get_add_form(type, passed_form = ''):

	form = ""

	if type == "library":
		form = AddLibraryItemForm(passed_form)

	
	return form
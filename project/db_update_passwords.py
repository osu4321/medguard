'''
Reset all passwords
'''

from views import db
from models import Users
from werkzeug.security import generate_password_hash, check_password_hash

all_users = Users.query.order_by(Users.user_id)

for user in all_users:

	user.password = generate_password_hash('12345')
	db.session.commit()


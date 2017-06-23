###########
# Models
##########

from views import db


'''
Users table
'''
class Users(db.Model):

	__tablename__ = 'users'

	user_id = db.Column(db.Integer, primary_key=True)
	last_name = db.Column(db.String(20), nullable=False)
	first_name = db.Column(db.String(20), nullable=False)
	sex = db.Column(db.String(1), nullable=False)
	dob = db.Column(db.Date, nullable=False)
	username = db.Column(db.String, unique=True, nullable=False)
	password = db.Column(db.String, nullable=False) # TODO Need this to be salted, etc
	email = db.Column(db.String, unique=True, nullable=False)
	phone_num = db.Column(db.String(10))
	user_level = db.relationship('User_level', backref='role')

	def __init__(self, last_name, first_name, sex, dob, username, password, email, phone_num):
		
		self.last_name = last_name
		self.first_name = first_name
		self.sex = sex
		self.dob = dob
		self.username = username
		self.password = password
		self.email = email
		self.phone_num = phone_num


	def __repr__(self):
		return '<User {0}>'.format(self.username)


'''
Users roles
'''
class User_level(db.Model):

	__tablename__ = 'user_level'

	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, primary_key=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False, primary_key=True)

	def __init__(self, user_id, role_id):

		self.user_id = user_id
		self.role_id = role_id

	def __repr__(self):
		return '<User_level {0}>'.format(self.role_id)


'''
Users roles
'''
class Roles(db.Model):

	__tablename__ = 'roles'

	role_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)

	def __init(self, role_id, name):

		self.role_id = role_id
		self.name = name

	def __repr__(self):
		return '<Role {0}>'.format(self.name)

'''
Patients
'''

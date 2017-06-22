# project/models.py



from views import db


'''
Users table
'''
class Users(db.model):

	__tablename__ = 'users'

	user_id = db.Column(db.Integer, primary_key=True)
	last_name = db.Column(db.String, nullable=False)
	first_name = db.Column(db.String, nullable=False)
	sex = db.Column(db.String(1), nullable=False)
	username = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False) # TODO Need this to be salted, etc
	email = db.Column(db.String)
	phone_num = db.Column(db.String(10))

	def __init__(self, user_id, last_name, first_name, sex, username, password, email, phone_num):
		self.user_id = user_id
		self.last_name = last_name
		self.first_name = first_name
		self.sex = sex
		self.username = username
		self.password = password
		self.email = email
		self.phone_num = phone_num


	def __repr__(self):
		return '<UserID {0}>'.format(self.user_id)



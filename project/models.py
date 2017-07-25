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
	password = db.Column(db.String, nullable=False)
	email = db.Column(db.String, unique=True, nullable=False)
	phone_num = db.Column(db.String(10))

	user_presc = db.relationship('UserMedications', foreign_keys = 'UserMedications.user_id', backref = 'user_presc')
	user_insur = db.relationship('UserInsurance', foreign_keys = 'UserInsurance.user_id', backref = 'user_insur')
	user_role = db.relationship('User_level', foreign_keys = 'User_level.user_id', backref = 'user_role')
	appts = db.relationship('PatientAppt', foreign_keys = 'PatientAppt.patient_id', backref = 'appts')
	doc = db.relationship('PatientAppt', foreign_keys = 'PatientAppt.doctor_id', backref = 'doc')

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
		return '<User_level {0}>'.format(self.user_id)


'''
Users roles
'''
class Roles(db.Model):

	__tablename__ = 'roles'

	role_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)

	role = db.relationship('User_level', foreign_keys = 'User_level.role_id', backref='role')

	def __init(self, role_id, name):

		self.role_id = role_id
		self.name = name

	def __repr__(self):
		return '<Role {0}>'.format(self.name)


'''
Patient Appointments
'''
class PatientAppt(db.Model):

	__tablename__ = 'patient_appt'

	appt_id = db.Column(db.Integer, primary_key=True)
	patient_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	doctor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	time = db.Column(db.Time, nullable=False)
	date = db.Column(db.Date, nullable=False)

	
	#doc = db.relationship('Users', foreign_keys='Users.user_id', backref='doc')

	def __init__(self, patient_id, doctor_id, date, time):
		
		self.patient_id = patient_id
		self.doctor_id = doctor_id
		self.date = date
		self.time = time
		
		
	def __repr__(self):
		return '<Appt {0}>'.format(self.appt_id)


'''
Appt Vitals table
'''
class ApptVitals(db.Model):

	__tablename__ = 'appt_vitals'

	vitals_id = db.Column(db.Integer, primary_key=True)
	appt_id = db.Column(db.Integer, db.ForeignKey('patient_appt.appt_id'), nullable=False)
	blood_pressure = db.Column(db.Integer, nullable=False)
	weight = db.Column(db.Integer, nullable=False)
	height = db.Column(db.Integer, nullable=False)
	notes = db.Column(db.String, nullable=False)

	def __init__(self, appt_id, blood_pressure, weight, height, notes):
		
		self.appt_id = appt_id
		self.blood_pressure = blood_pressure
		self.weight = weight
		self.height = height
		self.notes = notes


	def __repr__(self):
		return '<Vitals {0}>'.format(self.vitals_id)


'''
Medical Library table
'''
class MedLibrary(db.Model):

	__tablename__ = 'med_library'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	symptom = db.Column(db.String(200), nullable=False)
	excerpt = db.Column(db.String(100), nullable=False)
	desc = db.Column(db.String(500), nullable=False)

	
	def __init__(self, name, symptom, excerpt, desc):
		
		self.name = name
		self.symptom = symptom
		self.excerpt = excerpt
		self.desc = desc

	def __repr__(self):
		return '<Library {0}>'.format(self.id)


'''
Medications table
'''
class Medications(db.Model):

	__tablename__ = 'medications'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(1000), nullable=False)
	side_effects = db.Column(db.String(200), nullable=False)


	def __init__(self, name, description, side_effects):
		
		self.name = name
		self.description = description
		self.side_effects = side_effects

	def __repr__(self):
		return '<Library {0}>'.format(self.id)



'''
Insurance Provider table
'''
class InsuranceProvider(db.Model):

	__tablename__ = 'insurance_provider'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	address = db.Column(db.String(200), nullable=False)
	phone = db.Column(db.String(200), nullable=False)


	def __init__(self, name, address, phone):
		
		self.name = name
		self.address = address
		self.phone = phone

	def __repr__(self):
		return '<InsuranceProvider {0}>'.format(self.id)



'''
User Insurance table
'''
class UserInsurance(db.Model):

	__tablename__ = 'user_insurance'

	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False, primary_key = True)
	insurer_id = db.Column(db.Integer, db.ForeignKey('insurance_provider.id'), nullable = False, primary_key = True)
	policy_id = db.Column(db.Integer, nullable = False)
	plan_name = db.Column(db.String(50), nullable = False)
	coverage_date = db.Column(db.Date, nullable=False)

	def __init__(self, user_id, insurer_id, policy_id, plan_name, coverage_date):

		self.user_id = user_id
		self.insurer_id = insurer_id
		self.policy_id = policy_id
		self.plan_name = plan_name
		self.coverage_date = coverage_date


	def __repr__(self):
		return '<UserInsurance {0}>'.format(self.user_id)

'''
User Medications table
'''
class UserMedications(db.Model):

	__tablename__ = 'user_medications'

	id = db.Column(db.Integer, nullable = False, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
	med_id = db.Column(db.Integer, db.ForeignKey('medications.id'), nullable = False)
	prescribe_date = db.Column(db.Date, nullable=False)
	quantity = db.Column(db.Integer, nullable = False)
	exp_date = db.Column(db.Date, nullable=False)
	refill_amount = db.Column(db.Integer, nullable = False)
	refill_freq = db.Column(db.Integer, nullable = False)

	def __init__(self, user_id, med_id, prescribe_date, quantity, exp_date, refill_amount, refill_freq):

		self.user_id = user_id
		self.med_id = med_id
		self.prescribe_date = prescribe_date
		self.quantity = quantity
		self.exp_date = exp_date
		self.refill_amount = refill_amount
		self.refill_freq = refill_freq

	def __repr__(self):
		return '<UserMedication {0}>'.format(self.id)
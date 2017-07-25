###########
# Views
##########

from forms import AddTaskForm, RegisterForm, LoginForm, AddLibraryItemForm
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# Config
app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)


from models import Users, PatientAppt, User_level, MedLibrary, Medications, InsuranceProvider, UserMedications
from nav import render_nav, render_actions
from controller import ACCESS_LEVELS, get_add_form
from user import get_logged_in_user, logged_in_user_all


# Helper functions

'''
Login required decorator
'''
def login_required(test):

	@wraps(test)
	def wrap(*args, **kwargs):

		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first')
			return redirect(url_for('login'))

	return wrap


'''
Access level decorator
'''
def access_level(test):

	@wraps(test)
	def wrap(*args, **kwargs):

		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You do not have access to do that.')
			return redirect(url_for('dashboard'))

	return wrap



''' Time filter'''
def timeformat(value, format='%H:%M'):
	
    return value.strftime("%I:%M %p")

app.jinja_env.filters['timeformat'] = timeformat


''' Date filter'''
def dateformat(value, format='%H:%M'):
	
    return value.strftime("%m-%d-%Y")

app.jinja_env.filters['dateformat'] = dateformat


##########
# Route handlers
##########

'''
Register
'''
@app.route('/register/', methods=['GET', 'POST'])
def register():

	error = None
	form = RegisterForm(request.form)

	if request.method == 'POST':

		if form.validate_on_submit():

			# hash password
			hash_pass = generate_password_hash(form.password.data)

			# form new user
			new_user = Users(
				form.last_name.data,
				form.first_name.data,
				form.sex.data,
				form.dob.data,
				form.username.data,
				hash_pass,
				form.email.data,
				form.phone_num.data
			)

			# add new user to db
			db.session.add(new_user)

			# commit db
			db.session.commit()

			# message to user
			flash('Thanks for registering.  You may now login!')
			
			return redirect(url_for('login'))

		else :

			flash('Error in validation')


	# Wasn't post method, so show register template
	return render_template('register.html', form=form, error=error)


'''
Login
'''
@app.route('/', methods=['GET', 'POST'])
def login():

	error = None
	form = LoginForm(request.form)

	if request.method == 'POST':

		# TODO bug, never validates!
		#if form.validate_on_submit():

			user = Users.query.filter_by(username=request.form['username']).first()

			# If user exists and password matches
			if user is not None and check_password_hash(user.password, request.form['password']):

				session['logged_in'] = True
				session['user_id'] = user.user_id
				flash('Welcome to MEDGuard!')
			
				return redirect(url_for('view_user_dashboard'))

			else:

				error = "Invalid username or password."

		#else:

			#error = "All fields are required."

	return render_template('login.html', form=form, error=error)


'''
Logout
'''
@app.route('/logout')
def logout():

	session.pop('logged_in', None)
	flash('You\'ve been succssfully logged out.')

	return redirect(url_for('login'))


'''
View: User Dashboard
'''
@app.route('/dashboard/')
@login_required
def view_user_dashboard():

	data = ""

	
	return render_template('dashboard.html', main_nav = render_nav('main'), data=data, logged_user = logged_in_user_all())


'''
View: View Patients
'''
@app.route('/patients/')
@login_required
def view_patients():

	data = Users.query.order_by(Users.user_id)
	
	return render_template('patients.html', main_nav = render_nav('main'), data=data, page_title='Patients', logged_user = logged_in_user_all())


'''
View: View Single Patient
'''
@app.route('/patients/<user_id>')
@login_required
def view_single_patient(user_id):

	data = Users.query.filter(Users.user_id == user_id).first()
	# if (User_level.query.filter(User_level.user_id == data.user_id).first().role_id != ACCESS_LEVELS["doctor"]):
	# 	data = None
	# 	print("NOT A DOC")
	
	return render_template('patients-single.html', main_nav = render_nav('main'), data=data, logged_user = logged_in_user_all(), page_title='Patient: ' + data.first_name + ' ' + data.last_name)



'''
View: View Appointments
'''
@app.route('/appointments/')
@login_required
def view_appointments():

	data = PatientAppt.query.order_by(PatientAppt.date)
	page_title = "Appointments"

	return render_template('appointments.html', main_nav = render_nav('main'), data = data, logged_user = logged_in_user_all(), page_title = page_title)


'''
View: View My Appointments

'''
@app.route('/my_appointments/')
@login_required
def view_my_appointments():

	data = PatientAppt.query.filter_by(patient_id = get_logged_in_user('user_id')).order_by(PatientAppt.date)
	page_title = "Appointments"

	return render_template('appointments-patient.html', main_nav = render_nav('main'), data = data, logged_user = logged_in_user_all(), page_title = page_title)


'''
View: View Library
TODO actually get library info
'''
@app.route('/library/')
@login_required
def view_library():

	# TODO change to library info
	data = MedLibrary.query.order_by(MedLibrary.name)
	page_title = "Library"

	return render_template('library.html', main_nav = render_nav('main'), data = data, logged_user = logged_in_user_all(), page_title = page_title, action_nav = render_actions('library'))


'''
View: View Single Library
TODO actually get library info
'''
@app.route('/library/<item_id>')
@login_required
def view_single_library(item_id):

	# TODO change to library info
	data = MedLibrary.query.filter(MedLibrary.id == item_id).first()
	page_title = "Library"

	return render_template('library-single.html', main_nav = render_nav('main'), data = data, logged_user = logged_in_user_all(), page_title = page_title)


'''
View: View Insruance Providers
'''
@app.route('/insurance_providers/')
@login_required
def view_insurance_providers():

	data = InsuranceProvider.query.order_by(InsuranceProvider.name)
	page_title = "Insurance Providers"

	return render_template('insuranceproviders.html', main_nav = render_nav('main'), data = data, logged_user = logged_in_user_all(), page_title = page_title, action_nav = render_actions('insuranceprovider'))


'''
View: View Medications
'''
@app.route('/medications/')
@login_required
def view_medications():

	# TODO change to library info
	data = Medications.query.order_by(Medications.name)
	page_title = "Medications"

	return render_template('medications.html', main_nav = render_nav('main'), data = data, logged_user = logged_in_user_all(), page_title = page_title)


'''
View: View Single Medication
'''
@app.route('/medications/<item_id>')
@login_required
def view_single_medications(item_id):

	# TODO change to library info
	data = Medications.query.filter(Medications.id == item_id).first()
	page_title = "Medications"

	return render_template('medications-single.html', main_nav = render_nav('main'), data = data, logged_user = logged_in_user_all(), page_title = page_title)


'''
View: View My Medication
'''
@app.route('/my_medications')
@login_required
def view_my_medications():

	data = UserMedications.query.filter_by(user_id = get_logged_in_user('user_id')).order_by(UserMedications.prescribe_date)
	page_title = "My Medications"

	return render_template('medications-patient.html', main_nav = render_nav('main'), data = data, logged_user = logged_in_user_all(), page_title = page_title)


'''
View: Add item
'''
@app.route('/add/<type>', methods=['GET', 'POST'])
@login_required
def add_item(type):

	error = None
	page_title = "Add New"

	if request.method == 'POST':

		form = get_add_form(type, request.form)

		if form.validate_on_submit():

			# form new entry
			new_entry = MedLibrary(
				form.name.data,
				form.symptom.data,
				form.excerpt.data,
				form.desc.data
			)

			# add new entry to db
			db.session.add(new_entry)

			# commit db
			db.session.commit()

			# message to user
			flash('Entry successfully added.')
			
			return redirect(url_for('add_item', type=type))

		else :

			flash('Error in validation')

	else:
		form = get_add_form(type)
		
	template = 'add-' + type + '.html'
	return render_template(template, form = form, main_nav = render_nav('main'), logged_user = logged_in_user_all(), error = error, page_title = page_title)


####
# FROM TUTORIAL FOR REFERENCE
####

'''
Tasks
'''
# @app.route('/tasks/')
# @login_required
# def tasks():
	
# 	open_tasks = db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())
# 	closed_tasks = db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())

# 	return render_template('tasks.html', form = AddTaskForm(request.form), open_tasks = open_tasks, logged_user = logged_in_user_all(), closed_tasks = closed_tasks)


# '''
# Add new tasks
# '''
# @app.route('/add/', methods = ['POST'])
# @login_required
# def new_task():

# 	form = AddTaskForm(request.form)

# 	if request.method == 'POST':

# 		if form.validate_on_submit():

# 			new_task = Task(form.name.data, form.due_date.data, form.priority.data, '1')
# 			db.session.add(new_task)
# 			db.session.commit()
# 			flash("New entry successfully added.")

# 	return redirect(url_for('tasks'))


# '''
# Mark task as complete
# '''
# @app.route('/complete/<int:task_id>/')
# @login_required
# def complete(task_id):
	
# 	new_id = task_id
# 	db.session.query(Task).filter_by(task_id=new_id).update({"status":"0"})
# 	db.session.commit()
# 	flash("The task was marked as complete")
# 	return redirect(url_for('tasks'))


# '''
# Delete Tasks
# '''
# @app.route('/delete/<int:task_id>/')
# @login_required
# def delete_entry(task_id):
# 	new_id = task_id
# 	db.session.query(Task).filter_by(task_id=new_id).delete()
# 	db.session.commit()
# 	flash('The task was deleted.')
# 	return redirect(url_for('tasks'))



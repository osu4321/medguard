###########
# Views
##########

from forms import AddTaskForm, RegisterForm, LoginForm
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for, g
from flask_sqlalchemy import SQLAlchemy


# Config
app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)


from models import Users
from nav import render_nav

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
			
			# form new user
			new_user = Users(
				form.last_name.data,
				form.first_name.data,
				form.sex.data,
				form.dob.data,
				form.username.data,
				form.password.data,
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
			if user is not None and user.password == request.form['password']:

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
	flash('Goodbye!')

	return redirect(url_for('login'))


'''
View: User Dashboard
'''
@app.route('/dashboard/')
@login_required
def view_user_dashboard():

	return render_template('dashboard.html', main_nav = render_nav('main'))


'''
View: View Patients
'''
@app.route('/patients/')
@login_required
def view_patients():

	data = Users.query.order_by(Users.user_id)
	
	return render_template('patients.html', main_nav = render_nav('main'), data=data, page_title='Patients')


'''
View: View Single Patient
'''
@app.route('/patients/<user_id>')
@login_required
def view_single_patient(user_id):

	data = Users.query.filter(Users.user_id == user_id).first()
	
	return render_template('patients-single.html', main_nav = render_nav('main'), data=data, page_title='Patient: ' + data.first_name + ' ' + data.last_name)



'''
View: View Appointments
TODO actually get appointments
'''
@app.route('/appointments/')
@login_required
def view_appointments():

	data = Users.query.order_by(Users.user_id)
	page_title = "Appointments"

	return render_template('appointments.html', main_nav = render_nav('main'), data = data, page_title = page_title)


'''
View: View Library
TODO actually get library info
'''
@app.route('/library/')
@login_required
def view_library():

	# TODO change to library info
	data = Users.query.order_by(Users.user_id)
	page_title = "Library"

	return render_template('appointments.html', main_nav = render_nav('main'), data = data, page_title = page_title)





####
# FROM TUTORIAL FOR REFERENCE
####

'''
Tasks
'''
@app.route('/tasks/')
@login_required
def tasks():
	
	open_tasks = db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())
	closed_tasks = db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())

	return render_template('tasks.html', form = AddTaskForm(request.form), open_tasks = open_tasks, closed_tasks = closed_tasks)


'''
Add new tasks
'''
@app.route('/add/', methods = ['POST'])
@login_required
def new_task():

	form = AddTaskForm(request.form)

	if request.method == 'POST':

		if form.validate_on_submit():

			new_task = Task(form.name.data, form.due_date.data, form.priority.data, '1')
			db.session.add(new_task)
			db.session.commit()
			flash("New entry successfully added.")

	return redirect(url_for('tasks'))


'''
Mark task as complete
'''
@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
	
	new_id = task_id
	db.session.query(Task).filter_by(task_id=new_id).update({"status":"0"})
	db.session.commit()
	flash("The task was marked as complete")
	return redirect(url_for('tasks'))


'''
Delete Tasks
'''
@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
	new_id = task_id
	db.session.query(Task).filter_by(task_id=new_id).delete()
	db.session.commit()
	flash('The task was deleted.')
	return redirect(url_for('tasks'))
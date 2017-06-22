# forms

# imports
from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, SelectField, PasswordField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo


'''
Add a task!  For reference.... TODO remove
'''
class AddTaskForm(Form):

	task_id = IntegerField()
	name = StringField('Task Name', validators=[DataRequired()])
	due_date = DateField('Date Due (mm/dd/yyyy)', validators=[DataRequired()], format='%m/%d/%Y')
	priority = SelectField('Priority', validators=[DataRequired()], choices=[('1','1'),('2','2'),('3','3'),('4','4')])
	status = IntegerField('Status')


'''
User Registration
'''
class RegisterForm(Form):

	# Personal
	first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=20)])
	last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=20)])
	dob = DateField('Date of Birth', format='%Y-%m-%d')
	sex = RadioField('Sex', choices=[('m', 'Male'), ('f', 'Female')], validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Length(min=6, max=40)])
	phone_num = StringField('Phone Number (Just digits)', validators=[DataRequired(), Length(min=10, max=10)])

	# Account related
	username = StringField('Username', validators=[DataRequired(), Length(min=6, max=25)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
	confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])



'''
Login
'''
class LoginForm(Form):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
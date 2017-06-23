##########
# Navigation
##########

from flask import session, url_for
from controller import get_user_role


'''
Nav handler
'''
def render_nav(location):

	if location == "main":
		return render_nav_main()


'''
Main nav
'''
def render_nav_main():

	links = []

	user_id = session['user_id']
	role = get_user_role(user_id)

	# Add links to list based on role
	if role == 1:

		links.append(mg_get_link('patients'))
		links.append(mg_get_link('appointments'))

	# TODO expand on other roles
	#if role == '2':

	return links



'''
Links
'''
def mg_get_link(link):

	ret_vals = {}

	if link is 'patients':

		ret_vals['url'] = url_for('view_patients')
		ret_vals['name'] = 'Patients'
		ret_vals['icon'] = 'home'

	elif link == 'library':

		# TODO finish library link
		ret_vals['url'] = url_for('view_appointments')
		ret_vals['name'] = 'Appointments'
		ret_vals['icon'] = 'calendar'
		

	elif link == 'appointments':

		ret_vals['url'] = url_for('view_appointments')
		ret_vals['name'] = 'Appointments'
		ret_vals['icon'] = 'event'
		

	return ret_vals
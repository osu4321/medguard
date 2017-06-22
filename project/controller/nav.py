##########
# Navigation
##########

from flask import session

'''
Nav handler
'''
def render_nav(location):

	if location == "main":
		render_nav_main()


'''
Main nav
'''
def render_nav_main():

	user_id = session['user_id']

	role = get_user_role(user_id)

	if role == ''

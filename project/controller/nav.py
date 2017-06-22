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

	return "MAIN NAV"

##########
# Pages Data
##########

from flask import session, url_for

'''
Define which pages each role can access
'''
PAGE_ACCESS = {

	1 : [
		'library',
		'patients',
		'appointments',
		'medications',
		'insurance_providers'
		
	],

	2: [
		'my_appointments',
		'my_medications'
	],

	3: [],

	4: []

}
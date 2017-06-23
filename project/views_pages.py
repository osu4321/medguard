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
		'appointments'
		
	],

	2: [],

	3: [],

	4: []

}


'''
Define page meta
'''
'''
PAGE_META = {

	'patients' : {
		
		'url' : url_for('view_patients'),
		'title' : 'Patients',
		'icon' : 'home'
		
	}

}
'''
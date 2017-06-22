# create database


from views import db
from datetime import date
from models import Users
from datetime import date

# Create database and db table
db.create_all()

'''
Insert some preliminary data
'''

# Super User: superadmin/12345
db.session.add(Users("Smith", "John", "M", date(1970, 1, 1), "superadmin", "12345", "ellis.729@osu.edu", "1234567890"))
db.session.commit()

# Roles
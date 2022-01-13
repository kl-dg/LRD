from datetime import date
from datetime import datetime	

#From string to datetime

def yyyymmdd_to_datetime(value):
	"""
	Parses "YYYY/MM/DD" string to datetime object.
	"""
	
	if value: return datetime.strptime(value, '%Y/%m/%d')
		

def ddmmyyyy_to_datetime(value):
	"""
	Parses DD/MM/YYYY string to datetime object.
	"""
	
	if value:
		try:
			value = datetime.strptime(value, '%d/%m/%Y')
			return value
		except ValueError: return ""
		
		
def yyyymmddhhmmss_to_datetime(value):
	"""
	Parses "YYYY/MM/DD HH:mm:ss" string to datetime object
	"""
	
	if value: return datetime.strptime(value, '%Y/%m/%d %H:%M:%S')
	
#Calculations with dates
def days_elapsed_from_january_first():
	"""
	Returns number of days elapsed between today and January 1st of the
	current year.
	"""
	
	interval = datetime.now() - datetime.strptime(f'01/01/{datetime.now()}', '%d/%m/%Y')
	return interval.days

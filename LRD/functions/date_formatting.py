from datetime import date
from datetime import datetime

# Date generators
	

def get_now_time():
	"""
	Returns current date and time.
	"""
	
	return datetime.now()
	

def get_now_year():
	"""
	Returns current year.
	"""
	
	return get_now_time().strftime('%Y')


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
	
	interval = get_now_time() - datetime.strptime(f'01/01/{get_now_year()}', '%d/%m/%Y')
	return interval.days

# This file contains functions related to ISBN operations


#Validators
def isbn_10_validator(value):
	"""
	Checks if a INSB-10 is valid and returns True or False.
	"""

	if len(value) != 10: 
		return False
		
	try:
		int(value[0:9])
	except ValueError: 
		return False
		
	try:
		int(value[9])
	except ValueError:
		if value[9] == "X":
			pass
		elif value[9] == "x":
			value = f"{value[0:9]}X"
		else:
			return False
			
	index_counter = 10
	mod_sum = 0
	for digit in value[0:9]:
		mod_sum += int(digit) * index_counter
		index_counter -= 1
		
	try:
		mod_sum += int(value[9])
	except ValueError:
		mod_sum += 10
		
	if mod_sum % 11 == 0:
		return True
	else: 
		return False
		

def isbn_13_validator(value):
	"""
	Checks if a INSB-13 is valid and returns True or False.
	"""
	
	if len(value) != 13:
		return False
		
	index_counter = 0
	mod_sum = 0
	try: 
		for digit in value:
			if index_counter % 2 == 0:
				mod_sum += int(digit) * 1
			elif index_counter % 2 == 1:
				mod_sum += int(digit) * 3
			index_counter += 1
				
		if mod_sum % 10 == 0:
			return True
		else:
			return False
	except ValueError: 
		return False


#Autochecking and cleaning
def isbn_10_check(value):
	"""
	Validates ISBN-10 from GR import, returns blank value if it is not.
	"""
	
	value = value[2:12]
	if isbn_10_validator(value):
		if value[9] == "x":
			value = f"{value[0:9]}X"
		return value
	else: 
		value = ""
		return value

def isbn_13_check(value):
	"""
	Validates ISBN-13 from GR import, returns blank value if it is not
	"""
	
	value = value[2:15]
	if isbn_13_validator(value):
		return value
	else:
		value = ""
		return value

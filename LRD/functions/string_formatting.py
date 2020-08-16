from library.strings import available_formats

def author_import_from_gr(
		author_first_last, 
		author_last_first, 
		additional_authors, 
		name_order_choice, 
		import_additional_choice,
		):
			
	"""
	Formats authors from GR export file string to a list of authors.
	On user choice, use 'Last, First" or 'First Last' standard for
	name and import or not additional authors.
	"""
	
	author = []
	
	if name_order_choice: author.append(author_last_first)
	else: author.append(author_first_last)
	
	if import_additional_choice:
		if additional_authors:
			if name_order_choice:
				[author.append(f"{item.split()[-1]}, {' '.join(item.split()[0:-1])}".strip()) for item in additional_authors.split(',')]
			else:
				[author.append(item.strip()) for item in additional_authors.split(',')]
			
			
	return author
	

def format_binding(value):
	"""
	Adjusts GR import strings to this application standards.
	"""
	
	if value in available_formats: return value
	elif value == "Mass Market Paperback": return "Paperback"
	elif value == "Kindle Edition": return "Kindle Ebook"
	elif value == "Nook": return "Nook Ebook"
	elif value == "ebook": return "Ebook"
	elif value == "Audio CD": return "CD Audiobook"
	elif value == "Audio Cassete": return "Cassete Audiobook"
	elif value == "Audible Audio": return "Audiobook"
	elif value == "Leather Bound": return "Leatherbound"
	elif value == "Spiral-bound": return "Spiral"
	elif value == "Unknown Binding": return "Unknown"
	else: return "Unspecified"
	

def format_reading_status(value):
	"""
	Takes GR exclusive bookshelf field and fits into this application
	standards.
	"""
		
	if value == "read": return "Read"
	elif value == "currently-reading": return "Currently reading"
	elif value == "to-read": return "To read"
	

def format_condition(value_1, value_2):
	"""
	Merges condition columns from imported CSV into one string.
	"""
	
	if value_1 and value_2: return f"{value_1}, {value_2}"
	elif value_1 or value_2: return f"{value_1}{value_2}"
	else: return ""
		

def get_int(value):
	"""
	Returns value as int, except if it contains something else, 
	likely an empty string, which should return 0.
	"""
	
	try: return int(value)
	except (ValueError, TypeError): return 0 
		

def no_rating(value):
	"""
	Leaves "Rating" field empty in absence of rating in GR import.
	"""
	
	if value != "0": return value
	
	
def split_series_from_title(value):
	"""
	Splits title, series and volume in series when importing from
	GoodReads where syntax <Title (Series #n)> is found.
	"""
	   
	if "(" in value and ")" in value and "#" in value \
			and value.index("(") < value.index("#") < value.index(")"):
		open_parenthesis_index = value.index("(")
		close_parenthesis_index = value.index(")")
		number_sign_index = value.index("#")
		title = value[0:open_parenthesis_index]
		series = value[open_parenthesis_index+1: number_sign_index]
		volume = value[number_sign_index+1:close_parenthesis_index]
		if series[-2] == ',':
			series = series[0:len(series)-2]
		return [title.strip(), series.strip(), volume.strip()]
	else:
		return [value.strip(), "", ""]


def to_rating_cb(value):
	"""
	Appends the word "star" or "stars" to rating.
	"""
	
	prepend_to_stars = {"2", "3", "4", "5"}
	if value == "1": return "1 star"
	elif value in prepend_to_stars: return f"{value} stars"
	else: return "Not rated"
		



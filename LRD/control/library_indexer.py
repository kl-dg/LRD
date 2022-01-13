from data.libraries import books


def get_index():
	"""
	Gets an index for a newly added book.
	"""
	
	try:
		return max(books.keys()) + 1
	except (TypeError, ValueError):
		return 0
		
	

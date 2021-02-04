from library.book_library import library


def get_index():
	"""
	Gets an index for a newly added book.
	"""
	
	try:
		return max(library.keys()) + 1
	except (TypeError, ValueError):
		return 0
		
	

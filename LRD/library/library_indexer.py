from library.book_library import book_list


static_index_dict = dict()


def get_index():
	"""
	Gets an index for a newly added book.
	"""
	
	try:
		return max(book.static_index for book in book_list) + 1
	except (TypeError, ValueError):
		return 0
		

def get_index_list():
	"""
	Creates a list static library indexes.
	"""
	
	for index, book in enumerate(book_list):
		static_index_dict[book.static_index] = index
		
		
def refresh_index_list():
	"""
	Refreshes list of indexes.
	"""
	
	static_index_dict.clear()
	get_index_list()
	
		
	

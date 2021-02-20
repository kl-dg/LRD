from library.book_library import library

def delete_book(index):
	"""
	Deletes a book from the library.
	
	Parameter:
	index: book's index in the library.
	"""
	
	library.pop(index)

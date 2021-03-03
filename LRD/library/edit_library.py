from library.book_library import library

def delete_book(index):
	"""
	Deletes a book from the library.
	
	Parameter:
	index: book's index in the library.
	"""
	
	library.pop(index)
	

def edit_text_attribute(index, attribute, text):
	"""
	Changes value of text attributes (review, quotes and notes) of a book.
	
	Parameters:
	index: book index in library.
	
	attribute: "review", "quotes" or "notes".
	
	text: new value for book's attribute.
	"""
	
	setattr(library[index], attribute, text)


def reset_library():
	"""
	Remove all books from the library.
	
	Common uses: before loading a new library file or before starting a new library.
	"""
	
	library.clear()

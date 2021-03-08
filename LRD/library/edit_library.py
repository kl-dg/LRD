from library.book_library import library

def delete_book(index):
	"""
	Deletes a book from the library.
	
	Parameter:
	index: book's index in the library.
	"""
	
	library.pop(index)
	
	
def edit_attribute_value(old_value, new_value, attribute):
	"""
	Edits all ocurrences of an attribute value across the library.
	"""
	
	if attribute == 'author':
		for book in library.values():
			if old_value in book.author:
				if len(new_value) == 0:
					ocurrences_indexes = [i for i in range(len(book.author)) if book.author[i] == old_value]
					ocurrences_indexes.sort(reverse=True)
					for i in ocurrences_indexes:
						book.author.pop(i)
				else:
					book.author = [new_value if author == old_value else author for author in book.author]
	
	else:
		for book in library.values():
			if getattr(book, attribute) == old_value:
				setattr(book, attribute, new_value)
	

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

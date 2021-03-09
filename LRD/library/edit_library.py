from functions.date_formatting import get_now_time
from library.book_library import Book, library
from library.library_indexer import get_index

def add_or_edit_book(index, title, author, num_pages, publisher, rating, date_read, isbn_10, isbn_13, date_added,
		date_started, reading_status, book_format, review, edition_publication_year, original_publication_year,
		original_title, series, volume_in_series, collection, volume_in_collection, times_read, number_of_volumes,
		translator, weblink, bought_where, date_bought, bookshelves, condition, quotes, notes):
	"""
	Adds or edits a book on the library.
	
	If index is None, a new book will be added to the library. If an index is given, the book on the library index will
	be effectively overwritten by a new Book object containing the changed and the unchanged data.
	"""
	if index == None:
		index = get_index()
	
	library[index] = Book(
		title, 
		author, 
		num_pages, 
		publisher, 
		rating,
		date_read, 
		isbn_10,
		isbn_13,
		date_added if date_added is not None else get_now_time(),
		date_started,
		reading_status,
		book_format,
		review,
		edition_publication_year,
		original_publication_year,
		original_title,
		series,
		volume_in_series,
		collection,
		volume_in_collection,
		times_read,
		number_of_volumes,
		translator,
		weblink,
		bought_where,
		date_bought,
		bookshelves,
		condition,
		quotes,
		notes
		)
	

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

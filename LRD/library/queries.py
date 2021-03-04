from functions.value_calculations import average
from library.book_library import (library, 
	books_by_bookshelf_list, 
	books_by_publisher, 
	bookshelves_list, 
	reviews_list, 
	quotes_list, 
	notes_list
	)


def get_bookshelves_list():
	"""
	Refreshes list of bookshelves. 
	
	Finds every unique bookshelf in library and add to bookshelves list a dictionary containing
	the bookshelf name, book count, average rating and page count.
	"""
	
	#Clear current list of bookshelves
	bookshelves_list.clear()
	
	#Temporary dictionary for bookshelves stats
	bookshelves_dict = dict()
	
	#Loop through the library to get all unique shelves and their stats
	for book in library.values():
		for shelf in book.bookshelves:
			
			#If shelf not yet in bookshelves dict, add it
			if shelf not in bookshelves_dict:
				bookshelves_dict[shelf] = [0] * 5
			
			#Add bookshelves stats to dictionary
			bookshelves_dict[shelf][0] += 1
			if book.rating:
				bookshelves_dict[shelf][1] += int(book.rating)
				bookshelves_dict[shelf][2] += 1
			if book.num_pages:
				bookshelves_dict[shelf][3] += int(book.num_pages)
				bookshelves_dict[shelf][4] += 1
				
	#Add bookshelf dictionary to bookshelves list. Calculate average stats on the fly
	for key, value in bookshelves_dict.items():
		bookshelves_list.append(dict(
			bookshelf = key,
			book_count = value[0],
			average_rating = f"{average(value[1], value[2]):.2f}",
			average_length = f"{average(value[3], value[4]):.2f}",
			))
			

def get_books_by_bookshelf(selected_bookshelf):
	"""
	Refreshes list of books by selected bookshelf
	"""
	
	books_by_bookshelf_list.clear()
	[books_by_bookshelf_list.append(index) for index in library if selected_bookshelf in library[index].bookshelves]
				
				
def get_books_by_publisher(selected_publisher):
	"""
	Refreshes list of books by selected publisher
	"""
	
	books_by_publisher.clear()
	[books_by_publisher.append(index) for index in library if library[index].publisher == selected_publisher]
	
	
def get_books_with_text(book_attribute, output_list):
	"""
	Parameters:
	book_attribute: should be either "review", "quotes" or "notes".
	
	output_list: reference to review_list, quotes_list or notes_list.
	"""
	
	output_list.clear()
	for index in library:
		if getattr(library[index], book_attribute):
			output_list.append(index)


def get_list_by_attribute(working_list, attribute, get_avg_length = False):
	"""
	Fills a list with stats by attribute value. Works for attributes which value is a string, such as series,
	collections and publisher.
	
	args:		
	working_list: output list, such as publisherr_list.
	
	attribute: what book attribute, such as 'publisher'.
	
	get_avg_length: either True of False, depending if this information
	is relevant for the table.
	"""

	working_list.clear()
	attribute_dict = dict()
		
	for book in library.values():
		if getattr(book, attribute):
			if getattr(book, attribute) not in attribute_dict:
				attribute_dict[getattr(book, attribute)] = [0] * 5
				
			attribute_dict[getattr(book, attribute)][0] += 1
			if book.rating:
				attribute_dict[getattr(book, attribute)][1] += 1
				attribute_dict[getattr(book, attribute)][2] += int(book.rating)
			if book.num_pages and get_avg_length:
				attribute_dict[getattr(book, attribute)][3] += 1
				attribute_dict[getattr(book, attribute)][4] += int(book.num_pages)
	
	if get_avg_length:
		for key, value in attribute_dict.items():
			working_list.append(dict(
				title = key, 
				book_count = value[0],
				average_rating = f"{average(value[2], value[1]):.2f}",
				average_length = f"{average(value[4], value[3]):.2f}",
				))

	else:
		for key, value in attribute_dict.items():
			working_list.append(dict(
				title = key,
				book_count = value[0],
				average_rating = f"{average(value[2], value[1]):.2f}",
				))

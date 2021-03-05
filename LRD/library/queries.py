from functions.value_calculations import average
from library.book_library import (library, 
	books_by_bookshelf_list, 
	books_by_publisher, 
	books_read_by_year_list,
	bookshelves_list, 
	current_reading_list,
	gave_up_list,
	not_read_list,
	notes_list,
	quotes_list, 
	reviews_list, 
	research_books_list,
	to_read_list,
	wishlist,
	year_read_list,
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
				
def get_read_books_by_year(year):
	"""
	Refreshes list of books by year read.
	
	Parameter:
	year: either the year selected by the user or "No Read Date".
	"""
	
	books_read_by_year_list.clear()
	
	if year != "No Read Date":
		[books_read_by_year_list.append(index) for index in library if library[index].date_read and library[index].date_read.year == int(year)]
	else:
		[books_read_by_year_list.append(index) for index in library if not library[index].date_read]


def get_reading_status_lists():
	"""
	Refreshes lists by reading statuses.
	"""
	
	#Reset lists
	year_read_list.clear()
	current_reading_list.clear()
	to_read_list.clear()
	wishlist.clear()
	gave_up_list.clear()
	research_books_list.clear()
	not_read_list.clear()
	
	#Create temporary dict for yearly reading progress stats
	year_read_dict = dict()
	
	#Loop through the library and add indexes to list according to their reading status, except for books
	#marked as "Read", which information will be collected for reading progress table. 
	for index, book in library.items():
		if book.reading_status == "Read":
			if book.date_read:
				if str(book.date_read.year) not in year_read_dict:
					year_read_dict[str(book.date_read.year)] = [0] * 5
				
				year_read_dict[str(book.date_read.year)][0] += 1
				if book.rating:
					year_read_dict[str(book.date_read.year)][1] += 1
					year_read_dict[str(book.date_read.year)][2] += int(book.rating)
				if book.num_pages:
					year_read_dict[str(book.date_read.year)][3] += 1
					year_read_dict[str(book.date_read.year)][4] += int(book.num_pages)
					
			else:
				if "No Read Date" not in year_read_dict:
					year_read_dict["No Read Date"] = [0] * 5
					
				year_read_dict["No Read Date"][0] += 1
				if book.rating:
					year_read_dict["No Read Date"][1] += 1
					year_read_dict["No Read Date"][2] += int(book.rating)
				if book.num_pages:
					year_read_dict["No Read Date"][3] += 1
					year_read_dict["No Read Date"][4] += int(book.num_pages)
					
		elif book.reading_status == 'Currently reading':
			current_reading_list.append(index)
		elif book.reading_status == 'To read':
			to_read_list.append(index)
		elif book.reading_status == 'Wishlist':
			wishlist.append(index)
		elif book.reading_status == 'Gave up':
			gave_up_list.append(index)
		elif book.reading_status == 'For research':
			research_books_list.append(index)
		elif book.reading_status == 'Not read':
			not_read_list.append(index)
	
	#Transfer information from temporary dict to year_read_list, calculate averages on the fly
	for key, value in year_read_dict.items():
		year_read_list.append(dict(
			year = key, 
			book_count = value[0], 
			average_rating = f"{average(value[2], value[1]):.2f}",
			total_pages = str(value[4]), 
			average_length = f"{average(value[4], value[3]):.2f}",
			))


def get_read_books_general_statistics():
	"""
	Gets statistics for books read tab.
	
	Currently supported: 
	1 - Total books read;
	2 - Total pages read;
	3 - Average length (in pages);
	4 - Average rating (in stars).
	
	Return: a tuple with the information listed above.
	"""
	
	book_count = 0
	rating_count = 0
	rating_sum = 0
	length_count = 0
	length_sum = 0
	
	for book in library.values():
		if book.reading_status == 'Read':
			
			book_count += 1
			
			if book.rating:
				rating_count += 1
				rating_sum += int(book.rating)
				
			if book.num_pages:
				length_count+= 1
				length_sum += int(book.num_pages)

	return (book_count, length_sum, average(length_sum, length_count), average(rating_sum, rating_count))

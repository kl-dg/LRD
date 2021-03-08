from functions.date_formatting import get_now_year
from functions.value_calculations import average
from library.book_library import (library, 
	author_list,
	books_by_author_list,
	books_by_bookshelf_list, 
	books_by_publisher, 
	books_by_series_or_collection,
	books_by_year_list,
	books_read_by_year_list,
	bookshelves_list, 
	current_reading_list,
	gave_up_list,
	not_read_list,
	notes_list,
	quotes_list, 
	reviews_list, 
	research_books_list,
	search_list,
	to_read_list,
	wishlist,
	year_list,
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
	
	
def get_books_by_publishing_year(year, time_span, attribute):
	"""
	Refreshes books_by_year_list by getting all books published in the selected year / decade / century.
	
	Parameters:
	year: publishing year selected by user.
	
	time_span: either "year", "decade" or "century".
	
	attribute: either "original_publication_year" or "edition_publication_year"
	"""
	
	books_by_year_list.clear()
	
	if time_span == 'year':
		for index in library:
			if getattr(library[index], attribute) == year:
				books_by_year_list.append(index)
	
	elif time_span == 'decade':
		for index in library:
			if getattr(library[index], attribute):
				if 'older' in year:
					if int(getattr(library[index], attribute)) < int(f'{int(get_now_year()[0:-1]) - 20}0'):
						books_by_year_list.append(index)
				elif int(getattr(library[index], attribute)) >= int(year) and int(getattr(library[index], attribute)) < int(year) + 10:
					books_by_year_list.append(index)				
		
	elif time_span == 'century':
		for index in library:
			if getattr(library[index], attribute):
				if 'older' in year:
					if int(getattr(library[index], attribute)) <= int(f'{int(get_now_year()[0:-2]) - 10}00'):
						books_by_year_list.append(index)
				elif int(getattr(library[index], attribute)) > int(year) and int(getattr(library[index], attribute)) <= int(year) + 100:
					books_by_year_list.append(index)
					
					
def get_books_by_series_or_collection(title, attribute):
	"""
	Refreshes books_by_series_or_collection with a lists of books in the selected series or collection.
	"""
	
	books_by_series_or_collection.clear()
	[books_by_series_or_collection.append(index) for index in library if getattr(library[index], attribute) == title]
	
	
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
				
				
def get_list_of_authors():
	"""
	Refreshes author_list with the current list of authors found in the library and their stats (book count, average
	rating and book length).
	"""
	
	author_list.clear()
	
	author_dict = dict()
		
	for book in library.values():
		if len(book.author) > 0:
			for author in book.author:
				if author not in author_dict:
					author_dict[author] = [0] * 5
				
				author_dict[author][0] += 1
				if book.rating:
					author_dict[author][1] += int(book.rating)
					author_dict[author][2] += 1
				if book.num_pages:
					author_dict[author][3] += int(book.num_pages)
					author_dict[author][4] += 1
					
	for key, value in author_dict.items():
		author_list.append(dict(
			author = key,
			book_count = value[0],
			average_rating = f"{average(value[1], value[2]):.2f}",
			average_length = f"{average(value[3], value[4]):.2f}",
			))
				
				
def get_list_of_books_by_selected_author(author):
	"""
	Refreshes books_by_author_list by getting a list of books containing the author selected by user.
	"""
	
	books_by_author_list.clear()
		
	if author == "":
		[books_by_author_list.append(index) for index in library if len(library[index].author) == 0]
	
	else:
		[books_by_author_list.append(index) for index in library if author in library[index].author]
				

def get_pubyear_list(time_span, attribute):
	"""
	Refreshes year_list with a list of years, decades or centuries and its stats(book count and average rating).
	"""
	
	if time_span == 'year':
		get_list_by_attribute(year_list, attribute)
		
	elif time_span == 'decade':
		year_list.clear()
		
		year = get_now_year()
		cur_decade = int(f"{str(year)[0:-1]}0")
		decades_dict = dict()
		
		while cur_decade > int(year) - 209:
			decades_dict[f"{cur_decade}"] = [0, 0, 0]
			cur_decade -= 10
			
		decades_dict[f"{cur_decade + 9} or older"] = [0, 0, 0]
		
		for book in library.values():
			if getattr(book, attribute):
				try:
					decades_dict[f"{getattr(book, attribute)[0:-1]}0"][0] += 1
					if book.rating:
						decades_dict[f"{getattr(book, attribute)[0:-1]}0"][1] += 1
						decades_dict[f"{getattr(book, attribute)[0:-1]}0"][2] += int(book.rating)
				except KeyError:
					decades_dict[f"{cur_decade + 9} or older"][0] += 1
					if book.rating:
						decades_dict[f"{cur_decade + 9} or older"][1] += 1
						decades_dict[f"{cur_decade + 9} or older"][2] += int(book.rating)
						
		for key, value in decades_dict.items():
			if value[0] > 0:
				year_list.append(dict(
					title = key,
					book_count = value[0],
					average_rating = f"{average(value[2], value[1]):.2f}",
					))
		
	elif time_span == 'century':
		year_list.clear()
		
		year = get_now_year()
		cur_century = int(f"{str(year)[0:-2]}00")
		centuries_dict = dict()
		
		while cur_century > int(year) - 1099:
			centuries_dict[f"{cur_century}"] = [0, 0, 0]
			cur_century -= 100
			
		centuries_dict[f"{cur_century + 100} or older"] = [0, 0, 0]
		
		for book in library.values():
			if getattr(book, attribute):
				try:
					if not int(getattr(book, attribute)) % 100 == 0:
						centuries_dict[f"{getattr(book, attribute)[0:-2]}00"][0] += 1
						if book.rating:
							centuries_dict[f"{getattr(book, attribute)[0:-2]}00"][1] += 1
							centuries_dict[f"{getattr(book, attribute)[0:-2]}00"][2] += int(book.rating)
					elif int(getattr(book, attribute)) % 100 == 0:
						centuries_dict[f"{int(f'{getattr(book, attribute)[0:-2]}00') - 100}"][0] += 1
						if book.rating:
							centuries_dict[f"{int(f'{getattr(book, attribute)[0:-2]}00') - 100}"][1] += 1
							centuries_dict[f"{int(f'{getattr(book, attribute)[0:-2]}00') - 100}"][2] += int(book.rating)
				except KeyError:
					centuries_dict[f"{cur_century + 100} or older"][0] += 1
					if book.rating:
						centuries_dict[f"{cur_century + 100} or older"][1] += 1
						centuries_dict[f"{cur_century + 100} or older"][2] += int(book.rating)
						
		for key, value in centuries_dict.items():
			if value[0] > 0:
				year_list.append(dict(
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
	
	
def search_in_library(search_input, search_field, case_sensitive):
	"""
	Refreshes search_list with library indexes of all ocurrences of an attribute value.
	"""
	
	search_list.clear()
	
	if case_sensitive:
		if search_field.lower() != 'bookshelves' and search_field.lower() != 'author':
			for index in library:
				if search_input in getattr(library[index], search_field.lower()):
					search_list.append(index)
		else:
			for index in library:
				if search_input in "; ".join(getattr(library[index], search_field.lower())):
					search_list.append(index)
					
	elif not case_sensitive:
		if search_field.lower() != 'bookshelves' and search_field.lower() != 'author':
			for index in library:
				if search_input.lower() in getattr(library[index], search_field.lower()).lower():
					search_list.append(index)
		else:
			for index in library:
				if search_input.lower() in "; ".join(getattr(library[index], search_field.lower())).lower():
					search_list.append(index)	

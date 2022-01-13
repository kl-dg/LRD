from datetime import datetime

from functions.value_calculations import average

from data.libraries import (
	books,
	authors,
	bookshelves,
	collections,
	publishers,
	serieses,
	years,
	read_years,
	)

from data.index_lists import (
	search_results,
	books_by_selected_author,
	books_by_selected_series_or_collection,
	books_by_selected_publisher,
	books_by_selected_year,
	books_by_selected_bookshelf,
	books_current_reading,
	books_to_read,
	books_wishlisted,
	books_read_on_selected_year,
	books_given_up_reading,
	books_for_reasearch,
	books_not_read,
	)
	
	
def count_books_by_binding():
	"""
	Counts book on each format, physical, digital or audio. Returns a
	list of those formats with at least one book.
	"""
	
	count = dict()
	count['counts'] = [0, 0, 0]
	count['labels'] = ["Physical", "Digital", "Audio"]
	physical_formats = {'Paperback', 'Pocketbook', 'Hardcover', 
		'Leatherbound', 'Library Binding', 'Spiral', 'Custom binding',
		'Unbound'}
	digital_formats = {'Ebook', 'Kindle Ebook', 'Nook Ebook'}
	audio_formats = {'Audiobook', 'CD Audiobook', 'Cassete Audiobook'}
	for book in books.values():
		if book.book_format in physical_formats: count['counts'][0] += 1
		elif book.book_format in digital_formats: count['counts'][1] += 1
		elif book.book_format in audio_formats: count['counts'][2] += 1
		
	for index in reversed(range(0, 3)):
		if count['counts'][index] == 0:
			count['counts'].pop(index)
			count['labels'].pop(index)
	
	return count
	
	
def count_standalone_books():
	"""
	Returns a 2-item list with how many books are part of a series and how many are not.
	"""
	
	count = [0, 0]
	for book in books.values():
		if book.series: count[0] += 1
		else: count[1] += 1
	return count
	
	
def get_book_length_hist_data():
	"""
	Gets histogram data for page length with bin=100 up to 1000 pages
	long.
	"""
	
	count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	for book in books.values():
		try:
			if int(book.num_pages) < 1000: count[int(int(book.num_pages) / 100)] += 1
			elif int(book.num_pages) >= 1000: count[10] += 1
		except ValueError: continue
		
	return count


def get_bookshelves_list():
	"""
	Refreshes list of bookshelves. 
	
	Finds every unique bookshelf in library and add to bookshelves list a dictionary containing
	the bookshelf name, book count, average rating and page count.
	"""
	
	#Clear current list of bookshelves
	bookshelves.clear()
	
	#Temporary dictionary for bookshelves stats
	bookshelves_dict = dict()
	
	#Loop through the library to get all unique shelves and their stats
	for book in books.values():
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
		bookshelves.append(dict(
			bookshelf = key,
			book_count = value[0],
			average_rating = f"{average(value[1], value[2]):.2f}",
			average_length = f"{average(value[3], value[4]):.2f}",
			))
			

def get_books_by_bookshelf(selected_bookshelf):
	"""
	Refreshes list of books by selected bookshelf
	"""
	
	books_by_selected_bookshelf.clear()
	[books_by_selected_bookshelf.append(index) for index in books if selected_bookshelf in books[index].bookshelves]
				
				
def get_books_by_publisher(selected_publisher):
	"""
	Refreshes list of books by selected publisher
	"""
	
	books_by_selected_publisher.clear()
	[books_by_selected_publisher.append(index) for index in books if books[index].publisher == selected_publisher]
	
	
def get_books_by_publishing_year(year, time_span, attribute):
	"""
	Refreshes books_by_year_list by getting all books published in the selected year / decade / century.
	
	Parameters:
	year: publishing year selected by user.
	
	time_span: either "year", "decade" or "century".
	
	attribute: either "original_publication_year" or "edition_publication_year"
	"""
	
	books_by_selected_year.clear()
	
	if time_span == 'year':
		for index in books:
			if getattr(books[index], attribute) == year:
				books_by_selected_year.append(index)
	
	elif time_span == 'decade':
		for index in books:
			if getattr(books[index], attribute):
				if 'older' in year:
					if int(getattr(books[index], attribute)) < int(f'{int(datetime.now().strftime("%Y")[0:-1]) - 20}0'):
						books_by_selected_year.append(index)
				elif int(getattr(books[index], attribute)) >= int(year) and int(getattr(books[index], attribute)) < int(year) + 10:
					books_by_selected_year.append(index)				
		
	elif time_span == 'century':
		for index in books:
			if getattr(books[index], attribute):
				if 'older' in year:
					if int(getattr(books[index], attribute)) <= int(f'{int(datetime.now().strftime("%Y")[0:-2]) - 10}00'):
						books_by_selected_year.append(index)
				elif int(getattr(books[index], attribute)) > int(year) and int(getattr(books[index], attribute)) <= int(year) + 100:
					books_by_selected_year.append(index)
					
					
def get_books_by_series_or_collection(title, attribute):
	"""
	Refreshes books_by_series_or_collection with a lists of books in the selected series or collection.
	"""
	
	books_by_selected_series_or_collection.clear()
	[books_by_selected_series_or_collection.append(index) for index in books if getattr(books[index], attribute) == title]
	
	
def get_books_with_text(book_attribute, output_list):
	"""
	Parameters:
	book_attribute: should be either "review", "quotes" or "notes".
	
	output_list: reference to review_list, quotes_list or notes_list.
	"""
	
	output_list.clear()
	for index in books:
		if getattr(books[index], book_attribute):
			output_list.append(index)


def get_list_by_attribute(working_list, attribute, get_avg_length = False):
	"""
	Fills a list with stats by attribute value. Works for attributes which value is a string, such as series,
	collections and publisher.
	
	args:		
	working_list: output list, such as publisher_list.
	
	attribute: what book attribute, such as 'publisher'.
	
	get_avg_length: either True of False, depending if this information
	is relevant for the table.
	"""

	working_list.clear()
	attribute_dict = dict()
		
	for book in books.values():
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
				
				
def get_book_count_by_reading_status():
	"""
	Returns a dict with two lists, one for labels, another with the
	amount of books by reading statuses.
	"""
	
	status_count_dict = dict()

	for book in books.values():
		if book.reading_status not in status_count_dict:
			status_count_dict[book.reading_status] = 0
		status_count_dict[book.reading_status] += 1
	
	lib_composition_dict = dict()
	lib_composition_dict['labels'] = []
	lib_composition_dict['counts'] = []
	
	for key, count in status_count_dict.items():
		lib_composition_dict['labels'].append(key)
		lib_composition_dict['counts'].append(count)
		
	return lib_composition_dict
				
				
def get_list_of_authors():
	"""
	Refreshes author_list with the current list of authors found in the library and their stats (book count, average
	rating and book length).
	"""
	
	authors.clear()
	
	author_dict = dict()
		
	for book in books.values():
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
		authors.append(dict(
			author = key,
			book_count = value[0],
			average_rating = f"{average(value[1], value[2]):.2f}",
			average_length = f"{average(value[3], value[4]):.2f}",
			))
				
				
def get_list_of_books_by_selected_author(author):
	"""
	Refreshes books_by_author_list by getting a list of books containing the author selected by user.
	"""
	
	books_by_selected_author.clear()
		
	if author == "":
		[books_by_selected_author.append(index) for index in books if len(books[index].author) == 0]
	
	else:
		[books_by_selected_author.append(index) for index in books if author in books[index].author]
				

def get_pubyear_list(time_span, attribute):
	"""
	Refreshes year_list with a list of years, decades or centuries and its stats(book count and average rating).
	"""
	
	if time_span == 'year':
		get_list_by_attribute(years, attribute)
		
	elif time_span == 'decade':
		years.clear()
		
		year = datetime.now().strftime('%Y')
		cur_decade = int(f"{str(year)[0:-1]}0")
		decades_dict = dict()
		
		while cur_decade > int(year) - 209:
			decades_dict[f"{cur_decade}"] = [0, 0, 0]
			cur_decade -= 10
			
		decades_dict[f"{cur_decade + 9} or older"] = [0, 0, 0]
		
		for book in books.values():
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
				years.append(dict(
					title = key,
					book_count = value[0],
					average_rating = f"{average(value[2], value[1]):.2f}",
					))
		
	elif time_span == 'century':
		years.clear()
		
		year = datetime.now().strftime('%Y')
		cur_century = int(f"{str(year)[0:-2]}00")
		centuries_dict = dict()
		
		while cur_century > int(year) - 1099:
			centuries_dict[f"{cur_century}"] = [0, 0, 0]
			cur_century -= 100
			
		centuries_dict[f"{cur_century + 100} or older"] = [0, 0, 0]
		
		for book in books.values():
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
				years.append(dict(
					title = key,
					book_count = value[0],
					average_rating = f"{average(value[2], value[1]):.2f}",
					))
					
					
def get_rating_distribution():
	"""
	Counts the amount of books for each rating, 1 to 5.
	"""
	
	count = [0, 0, 0, 0, 0]
	for book in books.values():
		if book.rating: count[int(book.rating)-1] += 1
	return count
					
				
def get_read_books_by_year(year):
	"""
	Refreshes list of books by year read.
	
	Parameter:
	year: either the year selected by the user or "No Read Date".
	"""
	
	books_read_on_selected_year.clear()
	
	if year != "No Read Date":
		[books_read_on_selected_year.append(index) for index in books if books[index].date_read and books[index].date_read.year == int(year)]
	else:
		[books_read_on_selected_year.append(index) for index in books if not books[index].date_read]
		
		
def get_reading_progress_stats():
	"""
	Returns a dictionary of lists for year, amount of book read
	that year, pages read, average length, rating and pages read by day.
	"""
	
	def get_avg_pages_day(year, total_pages):
		"""
		Returns total pages read read in an year divided by amount of days.
		For current year, returns total pages read divided by days elapsed
		from the beginning of this year.
		"""

		if str(year) == datetime.now().strftime('%Y'):
			return total_pages / days_elapsed_from_january_first()
			
		elif year % 4 != 0:
			return total_pages / 365

		elif year % 4 == 0:
			return total_pages / 366
	
	content = dict()
	labels = []
	counts = []
	pages = []
	average_length = []
	average_rating = []
	average_pages_day = []
	
	if not read_years:
		get_reading_status_lists()
		
	year_read_list_ = read_years[:]
	year_read_list_.sort(key = lambda x: x['year'])
	
	for year_read in year_read_list_:
		if year_read['year'] != 'No Read Date':
			labels.append(year_read['year'])
			counts.append(year_read['book_count'])
			pages.append(int(year_read['total_pages']))
			average_length.append(float(year_read['average_length']))
			average_rating.append(float(year_read['average_rating']))
			average_pages_day.append(round(get_avg_pages_day(int(year_read['year']), int(year_read['total_pages'])), 1))
			
		
	content['labels'] = labels
	content['book_counts'] = counts
	content['pages'] = pages
	content['average_length'] = average_length
	content['average_rating'] = average_rating
	content['average_pages_day'] = average_pages_day
	
	return content


def get_reading_status_lists():
	"""
	Refreshes lists by reading statuses.
	"""
	
	#Reset lists
	read_years.clear()
	books_current_reading.clear()
	books_to_read.clear()
	books_wishlisted.clear()
	books_given_up_reading.clear()
	books_for_reasearch.clear()
	books_not_read.clear()
	
	#Create temporary dict for yearly reading progress stats
	year_read_dict = dict()
	
	#Loop through the library and add indexes to list according to their reading status, except for books
	#marked as "Read", which information will be collected for reading progress table. 
	for index, book in books.items():
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
			books_current_reading.append(index)
		elif book.reading_status == 'To read':
			books_to_read.append(index)
		elif book.reading_status == 'Wishlist':
			books_wishlisted.append(index)
		elif book.reading_status == 'Gave up':
			books_given_up_reading.append(index)
		elif book.reading_status == 'For research':
			books_for_reasearch.append(index)
		elif book.reading_status == 'Not read':
			books_not_read.append(index)
	
	#Transfer information from temporary dict to year_read_list, calculate averages on the fly
	for key, value in year_read_dict.items():
		read_years.append(dict(
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
	
	for book in books.values():
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
	
	search_results.clear()
	
	if case_sensitive:
		if search_field.lower() != 'bookshelves' and search_field.lower() != 'author':
			for index in books:
				if search_input in getattr(books[index], search_field.lower()):
					search_results.append(index)
		else:
			for index in books:
				if search_input in "; ".join(getattr(books[index], search_field.lower())):
					search_results.append(index)
					
	elif not case_sensitive:
		if search_field.lower() != 'bookshelves' and search_field.lower() != 'author':
			for index in books:
				if search_input.lower() in getattr(books[index], search_field.lower()).lower():
					search_results.append(index)
		else:
			for index in books:
				if search_input.lower() in "; ".join(getattr(books[index], search_field.lower())).lower():
					search_results.append(index)	

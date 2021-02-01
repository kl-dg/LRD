import csv

from functions.date_formatting import (
	get_now_time,
	yyyymmdd_to_datetime,
	yyyymmddhhmmss_to_datetime,
	)
from functions.isbn import isbn_10_check, isbn_13_check
from functions.string_formatting import (
	author_import_from_gr,
	format_binding,
	format_condition,
	format_reading_status,
	no_rating,
	split_series_from_title,
	)
from library.book_library import Book, book_list
from library.library_indexer import get_index
							   

def load_file(file_path):
	"""
	Loads a file previously saved with this program.
	"""
	
	with open(file_path, encoding='utf-8') as f:
		content = csv.reader(f)
		f.readline()
		loading_list = list()
		library_index = get_index()
		for line in content:
			loading_list.append(Book(
				line[1],
				[item.lstrip() for item in line[2].split(';') if len(item.strip()) > 0], 
				line[3], 
				line[4], 
				line[5], 
				yyyymmdd_to_datetime(line[6]),
				line[7],
				line[8],
				yyyymmddhhmmss_to_datetime(line[0]),
				yyyymmdd_to_datetime(line[11]),
				line[9],
				line[10],
				line[12],
				line[13],
				line[14],
				line[15],
				line[16],
				line[17],
				line[18],
				line[19],
				line[20],
				line[21],
				line[22],
				line[23],
				line[24],
				yyyymmdd_to_datetime(line[25]),
				[item.lstrip() for item in line[26].split(';')],
				line[27],
				line[28],
				line[29],
				library_index,
				))
			library_index += 1
		book_list.extend(loading_list)

def write_to_file(file_path):
	"""
	Writes book library to CSV file.
	"""
	
	with open(file_path, 'w', newline='', encoding='utf-8') as f:
		file_writer = csv.writer(
			f, 
			delimiter = ',', 
			quotechar='"', 
			escapechar = '\\'
			)
			
		file_writer.writerow([
			"Date Added",
			"Title",
			"Author", 
			"Number of Pages", 
			"Publisher", 
			"Rating", 
			"Date Read",
			"ISBN 10",
			"ISBN 13",
			"Reading Status",
			"Book Format",
			"Date Started",
			"Review",
			"Publication Year",
			"Original Publication Year",
			"Original Title",
			"Series",
			"Volume in Series",
			"Collection",
			"Volume in Collection",
			"Read Counter",
			"Number of Volumes",
			"Translator",
			"Weblink",
			"Bought At",
			"Date Bought",
			"Bookshelves",
			"Condition",
			"Quotes",
			"Notes",
			])
							  
		for item in book_list:
			file_writer.writerow([
				item.get_date_as_string('date_added', '%Y/%m/%d %H:%M:%S'),
				item.title, 
				'; '.join(item.author), 
				item.num_pages,
				item.publisher,
				item.rating,
				item.get_date_as_string('date_read', '%Y/%m/%d'),
				item.isbn10,
				item.isbn13,
				item.reading_status,
				item.book_format,
				item.get_date_as_string('date_started', '%Y/%m/%d'),
				item.review.replace("\n", "<br/>"),
				item.edition_publication_year,
				item.original_publication_year,
				item.original_title,
				item.series,
				item.volume_in_series,
				item.collection,
				item.volume_in_collection,
				item.times_read,
				item.number_of_volumes,
				item.translator,
				item.weblink,
				item.bought_where,
				item.get_date_as_string('date_bought', '%Y/%m/%d'),
				'; '.join(item.bookshelves),
				item.condition,
				item.quotes.replace("\n", "<br/>"),
				item.notes.replace("\n", "<br/>"),
				])


def import_from_file(file_path, last_name_first, additional_authors):
	"""
	Reads from Goodreads CSV export file and adds to book list.
	"""
	
	with open(file_path, encoding='utf-8') as f:
		content = csv.reader(f)
		f.readline()
		loading_list = list()
		library_index = get_index()
		for line in content:
			loading_list.append(Book(
				split_series_from_title(line[1])[0],
				author_import_from_gr(line[2], line[3], line[4], last_name_first, additional_authors),
				line[11], 
				line[9].strip(), 
				no_rating(line[7]), 
				yyyymmdd_to_datetime(line[14]),
				isbn_10_check(line[5]),
				isbn_13_check(line[6]),
				get_now_time(),
				"",
				format_reading_status(line[18]),
				format_binding(line[10]),
				line[19],
				line[12],
				line[13],
				"",
				split_series_from_title(line[1])[1],
				split_series_from_title(line[1])[2],
				"",
				"",
				line[22],
				"",
				"",
				"",
				line[27],
				line[26],
				[item.strip() for item in line[16].split(',')],
				format_condition(line[28], line[29]),
				"",
				line[21],
				library_index,
				))
			library_index += 1
		book_list.extend(loading_list)

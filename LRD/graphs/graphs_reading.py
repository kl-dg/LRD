from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget 

from functions.date_formatting import days_elapsed_from_january_first, get_now_year
from graphs.bar_charts import horizontal_bar_chart
from graphs.pie_charts import books_by_reading_status_pie_chart
from library.book_library import library, year_read_list


class GraphsWindowReadingTab(QWidget):
	"""
	Layout for reading progress graphs window.
	
	Window layout: let user scroll through the generated graphs.
	"""
	
	def __init__(self):
		super().__init__()
		self.setFixedSize(900, 720)
		self.setWindowModality(Qt.ApplicationModal)
		self.setWindowTitle("Reading progress in graphs")
		
		content = get_read_books_by_year()
		
		layout = QVBoxLayout()
		
		scrollable_content = QWidget()
		scrollable_content.setLayout(layout)
		
		v_scroll = QScrollArea(self)
		v_scroll.resize(900,720)
		v_scroll.setWidgetResizable(True)
		v_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		v_scroll.setWidget(scrollable_content)
		
		if count_books_read() > 0:
			layout.addWidget(horizontal_bar_chart(content['labels'], content['book_counts'], 
				"Books read by year"))
			layout.addWidget(horizontal_bar_chart(content['labels'], content['pages'],
				"Total pages read by year"))	
			layout.addWidget(horizontal_bar_chart(content['labels'], content['average_length'], 
				"Average book length by year \n In what years did I read longer books?"))				
			layout.addWidget(horizontal_bar_chart(content['labels'], content['average_rating'], 
				"Average rating by year"))
			layout.addWidget(horizontal_bar_chart(content['labels'], content['average_pages_day'], 
				"Average pages read by day"))
			layout.addWidget(books_by_reading_status_pie_chart(get_lib_composition()))
	
	
def count_books_read():
	"""
	Returns the amount of books which reading status is 'Read'.
	"""
	
	count = 0
	for book in library.values():
		if book.reading_status == 'Read': count += 1
	return count
	

def get_read_books_by_year():
	"""
	Returns a dictionary of lists for year value, amount of book read
	that year, pages read, average length, rating and pages read by day.
	"""
	
	content = dict()
	labels = []
	counts = []
	pages = []
	average_length = []
	average_rating = []
	average_pages_day = []
	
	year_read_list_ = year_read_list[:]
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
	


def get_avg_pages_day(year, total_pages):
	"""
	Returns total pages read read in an year divided by amount of days.
	For current year, returns total pages read divided by days elapsed
	from the beginning of this year.
	"""
	
	if str(year) == get_now_year():
		return total_pages / days_elapsed_from_january_first()
		
	elif year % 4 != 0:
		return total_pages / 365
	
	elif year % 4 == 0:
		return total_pages / 366
		
		
def get_lib_composition():
	"""
	Returns a dict with two lists, one for labels, another with the
	amount of books by reading statuses.
	"""
	
	status_set = set()
	for book in library.values():
		status_set.add(book.reading_status)
	
	status_count_dict = dict()
	for status in status_set:
		status_count_dict[status] = 0
		
	for book in library.values():
		status_count_dict[book.reading_status] += 1
	
	lib_composition_dict = dict()
	lib_composition_dict['labels'] = []
	lib_composition_dict['counts'] = []
	
	for key, count in status_count_dict.items():
		lib_composition_dict['labels'].append(key)
		lib_composition_dict['counts'].append(count)
		
	return lib_composition_dict

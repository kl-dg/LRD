from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget 

from functions.date_formatting import (
	days_elapsed_from_january_first, 
	get_now_year,
	)
from functions.value_calculations import bar_chart_text_pos_h
from library.book_library import book_list, year_read_list


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
		library_composition = get_lib_composition()
		
		layout = QVBoxLayout()
		
		scrollable_content = QWidget()
		scrollable_content.setLayout(layout)
		
		v_scroll = QScrollArea(self)
		v_scroll.resize(900,720)
		v_scroll.setWidgetResizable(True)
		v_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		v_scroll.setWidget(scrollable_content)
		
		if count_books_read() > 0:
			graph_books_by_year = HorizontalBarChart(
				content['labels'], 
				content['book_counts'], 
				"Books read by year",
				)
				
			layout.addWidget(graph_books_by_year)
			
			graph_pages_by_year = HorizontalBarChart(
				content['labels'], 
				content['pages'], 
				"Total pages read by year",
				)
				
			layout.addWidget(graph_pages_by_year)	
			
			average_length_by_year = HorizontalBarChart(
				content['labels'], 
				content['average_length'], 
				"Average book length by year \n In what years did I read longer books?",
			)
			
			layout.addWidget(average_length_by_year)
			
			average_rating_by_year = HorizontalBarChart(
				content['labels'], 
				content['average_rating'], 
				"Average rating by year",
				)
				
			layout.addWidget(average_rating_by_year)
		
			average_pages_read_day = HorizontalBarChart(
				content['labels'], 
				content['average_pages_day'], 
				"Average pages read by day",
				)
			layout.addWidget(average_pages_read_day)
			
			library_composition_by_status = GraphLibraryCompositionByStatus(library_composition)
			layout.addWidget(library_composition_by_status)
	
	
def count_books_read():
	"""
	Returns the amount of books which reading status is 'Read'.
	"""
	
	count = 0
	for book in book_list:
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
	for book in book_list:
		status_set.add(book.reading_status)
	
	status_count_dict = dict()
	for status in status_set:
		status_count_dict[status] = 0
		
	for book in book_list:
		status_count_dict[book.reading_status] += 1
	
	
	lib_composition_dict = dict()
	lib_composition_dict['labels'] = []
	lib_composition_dict['counts'] = []
	
	for key, count in status_count_dict.items():
		lib_composition_dict['labels'].append(key)
		lib_composition_dict['counts'].append(count)
		
	return lib_composition_dict
	
		

class HorizontalBarChart(FigureCanvasQTAgg):
	"""
	Creates a matplotlib horizontal bar chart.
	
	args: labels list, values list and title.
	"""
	
	def __init__(self, labels, values, title):
		figure = Figure(figsize=(8,len(labels)/3))
		bar_chart = figure.add_subplot(111)
		bar_chart.barh(labels, values, zorder=3)
		bar_chart.xaxis.grid(True, linestyle=':', zorder=0, alpha=0.3)
		bar_chart.set_title(title)
		
		max_value = max(values)
		
		for index, value in enumerate(values):
			if value < max_value / 10:
				bar_chart.text(
					value, 
					index, 
					" "+str(value),
					va='center', 
					color='tab:blue', 
					fontweight='bold', 
					size=9
					)
					
			elif value >= max_value / 10:
				bar_chart.text(
					bar_chart_text_pos_h(value, max_value),
					index, 
					str(value),
					va='center', 
					color='white', 
					fontweight='bold', 
					size=9
					)
			
		super().__init__(figure)
		self.setMinimumSize(self.size())


class GraphLibraryCompositionByStatus(FigureCanvasQTAgg):
	"""
	Creates a matplotlib pie chart.
	
	args: 
	content: dict with two lists, one for labels, other for values.
	"""
	
	def __init__(self, content):
		
		figure = Figure(figsize=(8,5))
		pie_chart = figure.add_subplot(111)
		pie_chart.pie(content['counts'], labels = content['labels'], autopct='%1.1f%%', shadow = True)
		pie_chart.set_title("Library composition by reading status")
		pie_chart.axis('equal')
		
		super().__init__(figure)
		self.setMinimumSize(self.size())
		

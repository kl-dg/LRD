from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget

from graphs.bar_charts import books_by_length_histogram, books_by_rating_vbar_chart
from graphs.pie_charts import books_in_series_vs_standalone_pie_chart, books_by_format_pie_chart
from library.book_library import library
from other_ui.gui_aggregators import matplotlib_pyqt_agg

class LibraryStatsGraphsWindow(QWidget):
	"""
	Layout for Library graphs window.
	
	Window layout: let user scroll through the generated graphs.
	"""
	
	def __init__(self):
		super().__init__()
		self.setFixedSize(900, 720)
		self.setWindowModality(Qt.ApplicationModal)
		self.setWindowTitle("Library in graphs")
				
		layout = QVBoxLayout()
		
		scrollable_content = QWidget()
		scrollable_content.setLayout(layout)
		
		v_scroll = QScrollArea(self)
		v_scroll.resize(900,720)
		v_scroll.setWidgetResizable(True)
		v_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		v_scroll.setWidget(scrollable_content)
		
		if len(library) > 0:
			layout.addWidget(matplotlib_pyqt_agg(books_in_series_vs_standalone_pie_chart(*count_standalone_books())))
			layout.addWidget(matplotlib_pyqt_agg(books_by_rating_vbar_chart(count_rating())))
			layout.addWidget(matplotlib_pyqt_agg(books_by_length_histogram(get_book_length_hist_data())))
			layout.addWidget(matplotlib_pyqt_agg(books_by_format_pie_chart(count_books_by_binding())))
		
		

def count_standalone_books():
	"""
	Returns a 2-item list with the amount of books in a series and how
	many are not.
	"""
	
	count = [0, 0]
	for book in library.values():
		if book.series: count[0] += 1
		else: count[1] += 1
	return count
	

def count_rating():
	"""
	Counts the amount of books for each rating, 1 to 5.
	"""
	
	count = [0, 0, 0, 0, 0]
	for book in library.values():
		if book.rating: count[int(book.rating)-1] += 1
	return count
	

def get_book_length_hist_data():
	"""
	Gets histogram data for page length with bin=100 up to 1000 pages
	long.
	"""
	
	count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	for book in library.values():
		try:
			if int(book.num_pages) < 1000: count[int(int(book.num_pages) / 100)] += 1
			elif int(book.num_pages) >= 1000: count[10] += 1
		except ValueError: continue
		
	return count
	
	
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
	for book in library.values():
		if book.book_format in physical_formats: count['counts'][0] += 1
		elif book.book_format in digital_formats: count['counts'][1] += 1
		elif book.book_format in audio_formats: count['counts'][2] += 1
		
	for index in reversed(range(0, 3)):
		if count['counts'][index] == 0:
			count['counts'].pop(index)
			count['labels'].pop(index)
	
	return count

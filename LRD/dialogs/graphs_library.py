from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget

from graphs.bar_charts import books_by_length_histogram, books_by_rating_vbar_chart
from graphs.pie_charts import books_in_series_vs_standalone_pie_chart, books_by_format_pie_chart
from library.book_library import library
from library.queries import count_books_by_binding, count_standalone_books, get_book_length_hist_data, get_rating_distribution
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
			layout.addWidget(matplotlib_pyqt_agg(books_by_rating_vbar_chart(get_rating_distribution())))
			layout.addWidget(matplotlib_pyqt_agg(books_by_length_histogram(get_book_length_hist_data())))
			layout.addWidget(matplotlib_pyqt_agg(books_by_format_pie_chart(count_books_by_binding())))
			

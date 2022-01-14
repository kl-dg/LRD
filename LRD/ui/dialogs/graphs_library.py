from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget

from control.queries import count_books_by_binding, count_standalone_books, get_book_length_hist_data, get_rating_distribution
from data.libraries import books
from ui.graphs.histogram_books_by_length import HistogramBooksByLength
from ui.graphs.pie_books_by_format import PieChartBooksByFormat
from ui.graphs.pie_books_in_series_vs_standalone import PieChartBooksInSeriesVsStandalone
from ui.graphs.vbar_books_by_rating import VBarChartBooksByRating
from ui.misc.gui_aggregators import matplotlib_pyqt_agg

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
		
		if len(books) > 0:
			layout.addWidget(matplotlib_pyqt_agg(PieChartBooksInSeriesVsStandalone(*count_standalone_books())))
			layout.addWidget(matplotlib_pyqt_agg(VBarChartBooksByRating(get_rating_distribution())))
			layout.addWidget(matplotlib_pyqt_agg(HistogramBooksByLength(get_book_length_hist_data())))
			layout.addWidget(matplotlib_pyqt_agg(PieChartBooksByFormat(count_books_by_binding())))
			

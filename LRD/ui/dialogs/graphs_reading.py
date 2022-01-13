from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget 

from ui.graphs.bar_charts import horizontal_bar_chart
from ui.graphs.pie_charts import books_by_reading_status_pie_chart
from control.queries import get_book_count_by_reading_status, get_read_books_general_statistics, get_reading_progress_stats
from ui.misc.gui_aggregators import matplotlib_pyqt_agg

class ReadingProgressGraphsWindow(QWidget):
	"""
	Layout for reading progress graphs window.
	
	Window layout: let user scroll through the generated graphs.
	"""
	
	def __init__(self):
		super().__init__()
		self.setFixedSize(900, 720)
		self.setWindowModality(Qt.ApplicationModal)
		self.setWindowTitle("Reading progress in graphs")
		
		reading_progress_data = get_reading_progress_stats()
		
		layout = QVBoxLayout()
		
		scrollable_content = QWidget()
		scrollable_content.setLayout(layout)
		
		v_scroll = QScrollArea(self)
		v_scroll.resize(900,720)
		v_scroll.setWidgetResizable(True)
		v_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		v_scroll.setWidget(scrollable_content)
		
		if get_read_books_general_statistics()[0] > 0:
			layout.addWidget(matplotlib_pyqt_agg(horizontal_bar_chart(reading_progress_data['labels'], 
				reading_progress_data['book_counts'], "Books read by year")))
			
			layout.addWidget(matplotlib_pyqt_agg(horizontal_bar_chart(reading_progress_data['labels'], 
				reading_progress_data['pages'], "Total pages read by year")))
				
			layout.addWidget(matplotlib_pyqt_agg(horizontal_bar_chart(reading_progress_data['labels'], 
				reading_progress_data['average_length'], 
				"Average book length by year \n In what years did I read longer books?")))
				
			layout.addWidget(matplotlib_pyqt_agg(horizontal_bar_chart(reading_progress_data['labels'], 
				reading_progress_data['average_rating'], "Average rating by year")))
			
			layout.addWidget(matplotlib_pyqt_agg(horizontal_bar_chart(reading_progress_data['labels'], 
				reading_progress_data['average_pages_day'], "Average pages read by day")))
			
			layout.addWidget(matplotlib_pyqt_agg(books_by_reading_status_pie_chart(get_book_count_by_reading_status())))

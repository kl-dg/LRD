from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from library.book_library import books_by_series_or_collection, collection_list, library, series_list
from library.queries import get_books_by_series_or_collection
from main_ui.main_window_proxy import main_window
from panel.refresh import refresh_panel
from panel.empty_panel import EmptyPanel
from tables.book_table import BookTable
from tables.series_table import SeriesTable


class SeriesTab(QWidget):
	"""
	Layout for Series tab in main window.
	
	Tab Layout:
	self.layout: divides screen horizontally, Info Panel on right side,
	tables on the left.
	
	self.tables_area: devides screen vertically, series and collection 
	tables on top, widget button on center, books b yseries or 
	collections on bottom.
	
	args:	
	attributes:
	self.selected_series: last clicked series, which books will be
	displayed in books by series table.
	
	self.selected_collection: last clicked collection, which books will 
	be displayed in books by series table.
	
	self.current_table: whether the last selection was a series or a
	collection.
	
	self.selected_book: last book clicked, for displaying in Info Panel.
	"""
	
	def __init__(self):
		super().__init__()
		self.is_outdated = True
		self.current_table = None
		self.selected_book = None
		
		self.series_table = SeriesTable(self, "series")
		self.collection_table = SeriesTable(self, "collection")
		self.books_by_series_table = BookTable(self, books_by_series_or_collection)
		
		button_edit_series = QPushButton("Edit selected series")
		button_edit_series.clicked.connect(lambda: self.clicked_edit_attribute(self.series_table, 'series'))
		
		button_no_series = QPushButton("Show standalone books")
		button_no_series.clicked.connect(self.get_standalone_books)
		
		button_edit_collection = QPushButton("Edit selected collection")
		button_edit_collection.clicked.connect(lambda: self.clicked_edit_attribute(self.collection_table, 'collection'))
		
		button_no_collection = QPushButton("Show books not in a collection")
		button_no_collection.clicked.connect(self.get_books_without_collection)
		
		series_collection_layout = QHBoxLayout()
		series_collection_layout.addWidget(self.series_table)
		series_collection_layout.addWidget(self.collection_table)
		
		widgets_area = QHBoxLayout()
		widgets_area.addWidget(button_edit_series)
		widgets_area.addWidget(button_no_series)
		widgets_area.addWidget(button_edit_collection)
		widgets_area.addWidget(button_no_collection)
		
		tables_area = QVBoxLayout()
		tables_area.addLayout(series_collection_layout)
		tables_area.addLayout(widgets_area)
		tables_area.addWidget(self.books_by_series_table)
		
		self.panel = EmptyPanel()
		
		self.layout = QHBoxLayout(self)
		self.layout.addLayout(tables_area)
		self.layout.addWidget(self.panel)
		

	def refresh_tab(self):
		"""
		When user comes back to this tab, refresh series, collection
		and books by series or collection tables as well as selected
		book's information in Info Panel.
		"""
		
		if self.is_outdated:
			self.series_table.refresh_table()
			self.collection_table.refresh_table()
			self.refresh_books_by_series_table()
			refresh_panel(self)
			self.is_outdated = False
		
		
	def reset_selections(self):
		"""
		When user loads other library, reset the selected series or 
		collection, selected book and list of books on the selected
		series or collection.
		"""
		
		self.series_table.selected_item = None
		self.collection_table.selected_item = None
		self.current_table = None
		self.selected_book = None
		books_by_series_or_collection.clear()
		self.books_by_series_table.refresh_table()
		
	
	def clicked_edit_attribute(self, table, attribute):
		"""
		Called when user clicks on "Edit Series" or "Edit Collection"
		button fo rbatch editing series or collections name.
		
		args:
		should be series_table, series_list and 'series' or 
		collection_table, collection_list and 'collection'.
		"""
		
		if table.selected_item:
			main_window.edit_attribute(table.selected_item, attribute)
		
			
	def get_standalone_books(self):
		"""
		Reset books by series or collection table, select books with 
		an empty 'series' attribute then calls 
		<self.get_books_by_series> to get a list of them.
		"""
		
		self.current_table = 'series'
		self.series_table.selected_item = ""
		self.refresh_books_by_series_table()
		
		
	def get_books_without_collection(self):
		"""
		Reset books by series or collection table, select books with 
		an empty 'collection' attribute then calls 
		<self.get_books_by_collection> to get a list of them.
		"""
		
		self.current_table = 'collection'
		self.collection_table.selected_item = ""
		self.refresh_books_by_series_table()
		
		
	def refresh_books_by_series_table(self):
		"""
		Refreshes list and table of books by selected series or collection. Pre-sort them by volume number.
		"""
		
		if self.current_table == 'series':
			get_books_by_series_or_collection(self.series_table.selected_item, 'series')
			books_by_series_or_collection.sort(key = lambda x: library[x].volume_in_series)
			
		elif self.current_table == 'collection':
			get_books_by_series_or_collection(self.collection_table.selected_item, 'collection')
			books_by_series_or_collection.sort(key = lambda x: library[x].volume_in_collection)
		
		self.books_by_series_table.refresh_table()

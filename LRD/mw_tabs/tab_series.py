from PyQt5.QtWidgets import (
	QHBoxLayout, 
	QPushButton,
	QVBoxLayout, 
	)

from library.book_library import (
	book_list,
	books_by_series_or_collection,
	collection_list, 
	series_list, 
	)
	 
from mw_tabs.main_window_tab import GenericMainWindowTab
from panel.refresh import refresh_panel
from panel.empty_panel import EmptyPanel
from tables.book_table import BookTable
from tables.series_table import SeriesTable


class SeriesTab(GenericMainWindowTab):
	"""
	Layout for Series tab in main window.
	
	Tab Layout:
	self.layout: divides screen horizontally, Info Panel on right side,
	tables on the left.
	
	self.tables_area: devides screen vertically, series and collection 
	tables on top, widget button on center, books b yseries or 
	collections on bottom.
	
	args:
	main_window: parent reference for using its methods.
	
	vars:
	self.selected_series: last clicked series, which books will be
	displayed in books by series table.
	
	self.selected_collection: last clicked collection, which books will 
	be displayed in books by series table.
	
	self.current_table: whether the last selection was a series or a
	collection.
	
	self.selected_book: last book clicked, for displaying in Info Panel.
	"""
	
	def __init__(self, main_window):
		super().__init__(main_window)
		self.selected_series = None
		self.selected_collection = None
		self.current_table = None
		self.selected_book = None
		
		self.series_table = SeriesTable(self, "series", self.get_series, series_list)
		self.collection_table = SeriesTable(self, "collection", self.get_collection, collection_list)
		self.books_by_series_table = BookTable(self, books_by_series_or_collection)
		
		button_edit_series = QPushButton("Edit selected series")
		button_edit_series.clicked.connect(lambda: self.clicked_edit_attribute(self.series_table, series_list, 'series'))
		
		button_no_series = QPushButton("Show standalone books")
		button_no_series.clicked.connect(self.get_standalone_books)
		
		button_edit_collection = QPushButton("Edit selected collection")
		button_edit_collection.clicked.connect(lambda: self.clicked_edit_attribute(self.collection_table, collection_list, 'collection'))
		
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
			if self.current_table == "series":
				self.get_books_by_series()
			elif self.current_table == "collection":
				self.get_books_by_collection()
			refresh_panel(self)
			self.is_outdated = False
		
		
	def reset_selections(self):
		"""
		When user loads other library, reset the selected series or 
		collection, selected book and list of books on the selected
		series or collection.
		"""
		
		self.selected_series = None
		self.selected_collection = None
		self.current_table = None
		self.selected_book = None
		books_by_series_or_collection.clear()
		self.books_by_series_table.refresh_table()
		
	
	def clicked_edit_attribute(self, table, list_, attribute):
		"""
		Called when user clicks on "Edit Series" or "Edit Collection"
		button fo rbatch editing series or collections name.
		
		args:
		should be series_table, series_list and 'series' or 
		collection_table, collection_list and 'collection'.
		"""
		
		index = [index.row() for index in table.selectionModel().selectedRows()]
		if index: 
			self.main_window.edit_attribute(list_[index[0]]['title'], attribute)
		
				
	def get_standalone_books(self):
		"""
		Reset books by series or collection table, select books with 
		an empty 'series' attribute then calls 
		<self.get_books_by_series> to get a list of them.
		"""
		
		books_by_series_or_collection.clear()
		self.current_table = 'series'
		self.selected_series = ""
		self.get_books_by_series()
		
		
	def get_books_without_collection(self):
		"""
		Reset books by series or collection table, select books with 
		an empty 'collection' attribute then calls 
		<self.get_books_by_collection> to get a list of them.
		"""
		
		books_by_series_or_collection.clear()
		self.current_table = 'collection'
		self.selected_collection = ""
		self.get_books_by_collection()


	def get_series(self):
		"""
		Gets selected series from series table then calls
		<self.get_books_by_series> to get a list of them.
		"""
		
		index = [index.row() for index in self.series_table.selectionModel().selectedRows()]
		if index:
			self.selected_series = series_list[index[0]]['title']
			self.current_table = 'series'
			self.get_books_by_series()
		
	def get_collection(self):
		"""
		Gets selected series from series table then calls
		<self.get_books_by_collection> to get a list of them.
		"""
		
		index = [index.row() for index in self.collection_table.selectionModel().selectedRows()]
		if index:
			self.selected_collection = collection_list[index[0]]['title']
			self.current_table = 'collection'
			self.get_books_by_collection()


	def get_books_by_series(self):
		"""
		Gets a list of all books on the selected series then calls
		<refresh_table> on books by series or collection table.
		"""
		
		books_by_series_or_collection.clear()
		for index, book in enumerate(book_list):
			if book.series == self.selected_series:
				books_by_series_or_collection.append(index)
				
		books_by_series_or_collection.sort(
			key = lambda x: book_list[x].volume_in_series
			)
			
		self.books_by_series_table.refresh_table()
		
		
	def get_books_by_collection(self):
		"""
		Gets a list of all books on the selected collection then calls
		<refresh_table> on books by series or collection table.
		"""
		
		books_by_series_or_collection.clear()
		for index, book in enumerate(book_list):
			if book.collection == self.selected_collection:
				books_by_series_or_collection.append(index)
				
		books_by_series_or_collection.sort(
			key = lambda x: book_list[x].volume_in_collection
			)
			
		self.books_by_series_table.refresh_table()

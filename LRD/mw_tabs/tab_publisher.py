from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout

from library.book_library import (
	book_list, 
	books_by_publisher, 
	publisher_list, 
	)
from mw_tabs.main_window_tab import GenericMainWindowTab
from panel.refresh import refresh_panel
from panel.empty_panel import EmptyPanel
from tables.book_table import BookTable
from tables.publisher_table import PublisherTable


class PublisherTab(GenericMainWindowTab):
	"""
	Layout for Publisher Tab in main window.
	
	Tab layout:
	self.layout: divides screen horizontally, Info Panel on right side,
	publisher table and books by publisher table on the left.
	
	self.tables_area: divides the screen vertically, top half for
	publishers table and widgets area, while bottom half for books by
	publisher table.
	
	self.publisher_table_area: divides the screen horizontally, left 
	side for publishers table, right side for widgets.
	
	args:
	main_window: parent reference for using its methods.
	
	attributes:
	self.selected_publisher: last publisher clicked by user, which books
	will be shown in books by publisher table.
	
	self.selected_book: last book clicked in books by publisher table,
	its full information will shown in Info Panel.
	"""
	
	def __init__(self, main_window):
		super().__init__(main_window)
		self.selected_publisher = None
		self.selected_book = None

		self.publisher_table = PublisherTable(self, publisher_list)
		self.books_by_publisher_table = BookTable(self, books_by_publisher)
		self.panel = EmptyPanel()
		
		button_edit_publisher = QPushButton("Edit selected publisher")
		button_edit_publisher.clicked.connect(self.clicked_edit_publisher)
		
		button_show_no_publisher = QPushButton("Show books without publisher")
		button_show_no_publisher.clicked.connect(self.get_books_without_publisher)
		
		widgets_area = QVBoxLayout()
		widgets_area.addWidget(button_edit_publisher)
		widgets_area.addWidget(button_show_no_publisher)
		
		publisher_table_area = QHBoxLayout()
		publisher_table_area.addWidget(self.publisher_table, 7)
		publisher_table_area.addLayout(widgets_area, 4)

		tables_area = QVBoxLayout()
		tables_area.addLayout(publisher_table_area)
		tables_area.addWidget(self.books_by_publisher_table)
		
		self.layout = QHBoxLayout(self)
		self.layout.addLayout(tables_area)
		self.layout.addWidget(self.panel)
		
		
	def refresh_tab(self):
		"""
		When user comes back to this tab, refresh publisher and books 
		by publisher tables and selected book's information in Info 
		Panel.
		"""
		
		if self.is_outdated:
			self.publisher_table.refresh_table()
			self.get_books_by_publisher()
			refresh_panel(self)
			self.is_outdated = False
		
		
	def reset_selections(self):
		"""
		When user opens other library file, reset selected publisher
		and selected book.
		"""
		self.selected_publisher = None
		self.selected_book = None
		
		
	def clicked_edit_publisher(self):
		"""
		Batch edit publisher's name.
		Gets publisher's index at publisher's table then send it edit
		attribute batch name editor dialog.
		"""
		
		index = [index.row() for index in self.publisher_table.selectionModel().selectedRows()]
		if index:
			self.main_window.edit_attribute(publisher_list[index[0]]['title'], 'publisher')
			
			
	def get_publisher(self):
		"""
		Gets clicked publisher in publisher table and calls method
		to get a list of its books.
		"""
		
		index = [index.row() for index in self.publisher_table.selectionModel().selectedRows()]
		if index:
			self.selected_publisher = publisher_list[index[0]]['title']
			self.get_books_by_publisher()
			
			
	def get_books_without_publisher(self):
		"""
		In order to get a list of books wit han empty publisher 
		attribute, set an empty string to selected book and refresh
		list of books by publisher.
		"""
		
		self.selected_publisher = ""
		self.get_books_by_publisher()
			
			
	def get_books_by_publisher(self):
		"""
		Refreshes list of books by selected publisher then call
		<refresh_table> on books by publisher table.
		"""
		
		books_by_publisher.clear()
		for index_, book in enumerate(book_list):
			if book.publisher == self.selected_publisher:
				books_by_publisher.append(index_)
				
		self.books_by_publisher_table.refresh_table()

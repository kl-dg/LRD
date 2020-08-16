from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
	
from functions.value_calculations import average
from library.book_library import (
	bookshelves_list, 
	book_list, 
	books_by_bookshelf_list, 
	)
from mw_tabs.main_window_tab import GenericMainWindowTab
from panel.refresh import refresh_panel
from panel.empty_panel import EmptyPanel
from tables.bookshelves_table import BookshelvesTable
from tables.book_table import BookTable


class BookshelvesTab(GenericMainWindowTab):
	"""
	Layout for Bookshelves tab in main window.
	
	Tab Layout: 
	self.layout: divides the screen horizontally, right side for book's
	information panel. Left side for tables and widgets.
	
	self.tables_area_layout: divides the screen vertically, bookshelves
	stats table and widgets on top, books by bookshelf on bottom.
	
	args:
	main_window: parent reference for using its methods.
	
	attributes:
	self.selected_bookshelf: selected bookshelf by user, of which books
	will be shown in books by bookshelf table.
	
	self.selected_book: last book selected by user, which information
	will be displayed in Info Panel.
	"""
	
	def __init__(self, main_window):
		super().__init__(main_window)
		self.selected_bookshelf = None
		self.selected_book = None
		
		self.bookshelves_table = BookshelvesTable(self, bookshelves_list)
		
		bookshelves_table_area = QHBoxLayout()
		bookshelves_table_area.addWidget(self.bookshelves_table)
		
		self.books_by_bookshelf_table = BookTable(self, books_by_bookshelf_list)
		
		tables_area_layout = QVBoxLayout()
		tables_area_layout.addLayout(bookshelves_table_area)
		tables_area_layout.addWidget(self.books_by_bookshelf_table)
		
		self.panel = EmptyPanel()
		
		self.layout = QHBoxLayout(self)
		self.layout.addLayout(tables_area_layout)
		self.layout.addWidget(self.panel)


	def refresh_tab(self):
		"""
		When user comes back to this table, refresh bookshelves stats
		table, books by selected shelf table and information panel of
		selected book.
		"""
		
		if self.is_outdated:
			self.bookshelves_table.refresh_table()
			self.get_books_by_bookshelf()
			refresh_panel(self)
			self.is_outdated = False
		
		
	def reset_selections(self):
		"""
		When user opens other library file, reset selected shelf and
		selected book.
		"""
		
		self.selected_bookshelf = None
		self.selected_book = None
		
		
	def get_list_by_attribute(self):
		"""
		Fills bookshelves list with all unique bookshelves, books 
		counts, average rating and length.
		"""
		
		bookshelves_list.clear()
		
		bookshelves_set = set()
		for book in book_list:
			if len(book.bookshelves) > 1 or book.bookshelves[0]:
				for shelf in book.bookshelves:
					bookshelves_set.add(shelf)
					
		bookshelves_dict = dict()
		for shelf in bookshelves_set:
			bookshelves_dict[shelf] = [0, 0, 0, 0, 0]
			
		for book in book_list:
			if len(book.bookshelves) > 1 or book.bookshelves[0]:
				for shelf in book.bookshelves:
					bookshelves_dict[shelf][0] += 1
					if book.rating:
						bookshelves_dict[shelf][1] += int(book.rating)
						bookshelves_dict[shelf][2] += 1
					if book.num_pages:
						bookshelves_dict[shelf][3] += int(book.num_pages)
						bookshelves_dict[shelf][4] += 1
						
		for key, value in bookshelves_dict.items():
			bookshelves_list.append(dict(
				bookshelf = key,
				book_count = value[0],
				average_rating = f"{average(value[1], value[2]):.2f}",
				average_length = f"{average(value[3], value[4]):.2f}",
				))
		
		
	def get_selected_bookshelf(self):
		"""
		Gets selected shelf and calls function to get a list of books
		with a matching bookshelf attribute.
		"""
		
		index = [index.row() for index in self.bookshelves_table.selectionModel().selectedRows()]
		if index:
			self.selected_bookshelf = bookshelves_list[index[0]]['bookshelf']
			self.get_books_by_bookshelf()
			
			
	def get_books_by_bookshelf(self):
		"""
		Gets a list of books with a bookshelf attribute that matches 
		user's selection, then calls <refresh_table> on books by
		selected bookshelf table.
		"""
		
		books_by_bookshelf_list.clear()
		for index_, book in enumerate(book_list):
			if self.selected_bookshelf in book.bookshelves:
				books_by_bookshelf_list.append(index_)
				
		self.books_by_bookshelf_table.refresh_table()

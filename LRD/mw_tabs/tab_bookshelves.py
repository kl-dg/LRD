from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from library.book_library import books_by_bookshelf_list
from library.queries import get_books_by_bookshelf
from panel.refresh import refresh_panel
from panel.empty_panel import EmptyPanel
from tables.bookshelves_table import BookshelvesTable
from tables.book_table import BookTable


class BookshelvesTab(QWidget):
	"""
	Layout for Bookshelves tab in main window.
	
	Tab Layout: 
	self.layout: divides the screen horizontally, right side for book's
	information panel. Left side for tables and widgets.
	
	self.tables_area_layout: divides the screen vertically, bookshelves
	stats table and widgets on top, books by bookshelf on bottom.
	
	attributes:
	self.selected_book: last book selected by user, which information
	will be displayed in Info Panel.
	"""
	
	def __init__(self):
		super().__init__()
		self.is_outdated = True
		self.selected_book = None
		
		self.bookshelves_table = BookshelvesTable(self)
		
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
			self.refresh_books_by_bookshelf_table()
			refresh_panel(self)
			self.is_outdated = False
		
		
	def reset_selections(self):
		"""
		When user opens other library file, reset selected shelf and
		selected book.
		"""
		
		self.bookshelves_table.selected_bookshelf = None
		self.selected_book = None
		
		
	def refresh_books_by_bookshelf_table(self):
		"""
		Calls get_books_by_bookshelf() to refresh the list of books by selected bookshelf then
		refresh the books by bookshelf table.
		"""
		
		get_books_by_bookshelf(self.bookshelves_table.selected_bookshelf)
		self.books_by_bookshelf_table.refresh_table()

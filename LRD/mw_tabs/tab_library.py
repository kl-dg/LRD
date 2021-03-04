from PyQt5.QtWidgets import QHBoxLayout, QWidget

from library.book_library import library
from panel.refresh import refresh_panel
from panel.empty_panel import EmptyPanel
from tables.book_table import BookTable


class LibraryTab(QWidget):
	"""
	Layout for Library Tab in main window.
	
	Tab layout:
	self.layout: splits screen in half, left side for Info
	Panel, left side a table to display all books in the library.

	attributes:
	self.selected_book: last book clicked, for displaying in Info Panel.
	
	self.all_indexes: as Library Tab should display all books, this list
	must have indexes for the entire library.
	"""
	
	def __init__(self):
		super().__init__()
		self.is_outdated = True
		self.selected_book = None
		self.all_indexes = []
		
		self.table = BookTable(self, self.all_indexes)
		self.panel = EmptyPanel()

		self.layout = QHBoxLayout(self)
		self.layout.addWidget(self.table)
		self.layout.addWidget(self.panel)
		
		
	def refresh_tab(self):
		"""
		When user comes back to library tab, update table and refresh
		Info Panel.
		"""
		
		if self.is_outdated:
			self.get_all_indexes()
			self.table.refresh_table()
			refresh_panel(self)
			self.is_outdated = False
		
		
	def get_all_indexes(self):
		"""
		Generates a list of indexes the length of the library. 
		"""
		
		self.all_indexes.clear()
		self.all_indexes.extend(list(library.keys()))
		
		
	def reset_selections(self):
		"""
		When user opens other library, reset Info Panel.
		"""
		
		self.selected_book = None
		

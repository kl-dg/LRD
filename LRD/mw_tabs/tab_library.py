from PyQt5.QtWidgets import QHBoxLayout

from library.book_library import book_list
from mw_tabs.main_window_tab import GenericMainWindowTab
from panel.refresh import refresh_panel
from panel.empty_panel import EmptyPanel
from tables.book_table import BookTable


class LibraryTab(GenericMainWindowTab):
	"""
	Layout for Library Tab in main window.
	
	Tab layout:
	self.layout: splits screen in half, left side for Info
	Panel, left side a table to display all books in the library.
	
	args:
	main_window: parent reference for using its methods.
	
	attributes:
	self.selected_book: last book clicked, for displaying in Info Panel.
	
	self.all_indexes: as Library Tab should display all books, this list
	will have indexes for the entire library.
	"""
	
	def __init__(self, main_window):
		super().__init__(main_window)
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
		for index in range(0, len(book_list)):
			self.all_indexes.append(index)
		
		
	def reset_selections(self):
		"""
		When user opens other library, reset Info Panel.
		"""
		
		self.selected_book = None
		

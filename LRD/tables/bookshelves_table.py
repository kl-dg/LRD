from PyQt5.QtWidgets import QTableWidgetItem

from library.book_library import bookshelves_list
from library.queries import get_bookshelves_list
from tables.generic_table import GenericTable

class BookshelvesTable(GenericTable):
	"""
	Table for book bookshelves stats.
	
	args:
	get_books: function that gets books by selected shelf.
	
	attributes:
	self.current_sorting: column selected for sorting table.
	self.parent_tab: window tab where this table is inserted to.
	self.selected_bookshelf: last bookshelf selected by user.
	"""
	
	def __init__(self, parent_tab):
		super().__init__(column_count = 4)
		self.current_sorting = '1'
		self.parent_tab = parent_tab
		self.selected_bookshelf = None
		
		self.itemSelectionChanged.connect(self.bookshelf_selection_changed)
		self.setHorizontalHeaderLabels((
			"Bookshelf",
			"Books",
			"Average Rating",
			"Average Length",
			))
		self.setColumnWidth(0,250)
		self.setColumnWidth(1,50)
		self.setColumnWidth(2,100)
		self.setColumnWidth(3,100)
		
		
	def get_selected_bookshelf(self):
		"""
		Returns the name of the selected bookshelf.
		"""
		
		index = [index.row() for index in self.selectionModel().selectedRows()]
		if index:
			return bookshelves_list[index[0]]['bookshelf']
			
			
	def bookshelf_selection_changed(self):
		"""
		When user selects other bookshelf in bookshelves table, store its name in
		self.selected_bookshelf then refresh books by selected bookshelf table.
		"""
		
		if self.get_selected_bookshelf():
			self.selected_bookshelf = self.get_selected_bookshelf()
			self.parent_tab.refresh_books_by_bookshelf_table()
		
		
	def refresh_table(self, sorting=False):
		"""
		Calls function to get a list of bookshelves, unless refreshing
		after sorting. Add list contents to table.
		"""
		
		if not sorting:
			get_bookshelves_list()
		self.sort_table(self.current_sorting)
		self.setRowCount(0)
		for entry in bookshelves_list:
			bookshelf = QTableWidgetItem(entry['bookshelf'])
			book_count = QTableWidgetItem(str(entry['book_count']))
			average_rating = QTableWidgetItem(entry['average_rating'])
			average_length = QTableWidgetItem(entry['average_length'])
			
			row = self.rowCount()
			self.insertRow(row)
			self.setItem(row, 0, bookshelf)
			self.setItem(row, 1, book_count)
			self.setItem(row, 2, average_rating)
			self.setItem(row, 3, average_length)
		
	
	def sort_table(self, mode):
		"""
		Sorts table by selected column/attribute, then calls
		<refresh_table>.
		
		args:
		mode: column index and whether reverse order or not.
		"""
		
		if mode == '0r': bookshelves_list.sort(key = lambda x: x['bookshelf'].lower(), reverse=True)
		elif mode == '0': bookshelves_list.sort(key = lambda x: x['bookshelf'].lower())	
		elif mode == '1r': bookshelves_list.sort(key = lambda x: x['book_count'])
		elif mode == '1': bookshelves_list.sort(key = lambda x: x['book_count'], reverse=True)
		elif mode == '2r': bookshelves_list.sort(key = lambda x: float(x['average_rating']), reverse=True)
		elif mode == '2': bookshelves_list.sort(key = lambda x: float(x['average_rating']))
		elif mode == '3r': bookshelves_list.sort(key = lambda x: float(x['average_length']))
		elif mode == '3': bookshelves_list.sort(key = lambda x: float(x['average_length']), reverse=True)

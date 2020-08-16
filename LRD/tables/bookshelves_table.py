from PyQt5.QtWidgets import QTableWidgetItem

from tables.generic_table import GenericTable

class BookshelvesTable(GenericTable):
	"""
	Table for book bookshelves stats.
	
	args:
	get_books: function that gets books by selected shelf.
	
	source_list: list with contents to be loaded into the table.
	
	attributes:
	self.current_sorting: column selected for sorting table.
	"""
	
	def __init__(self, parent, source_list):
		super().__init__(column_count = 4)
		self.parent = parent
		self.source_list = source_list
		self.current_sorting = '1'
		
		self.itemSelectionChanged.connect(self.parent.get_selected_bookshelf)
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
		
		
	def refresh_table(self, sorting=False):
		"""
		Calls function to get a list of bookshelves, unless refreshing
		after sorting. Add list contents to table.
		"""
		
		if not sorting:
			self.parent.get_list_by_attribute()
		self.sort_table(self.current_sorting)
		self.setRowCount(0)
		for entry in self.source_list:
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
		
		if mode == '0r': self.source_list.sort(key = lambda x: x['bookshelf'].lower(), reverse=True)
		elif mode == '0': self.source_list.sort(key = lambda x: x['bookshelf'].lower())	
		elif mode == '1r': self.source_list.sort(key = lambda x: x['book_count'])
		elif mode == '1': self.source_list.sort(key = lambda x: x['book_count'], reverse=True)
		elif mode == '2r': self.source_list.sort(key = lambda x: float(x['average_rating']), reverse=True)
		elif mode == '2': self.source_list.sort(key = lambda x: float(x['average_rating']))
		elif mode == '3r': self.source_list.sort(key = lambda x: float(x['average_length']))
		elif mode == '3': self.source_list.sort(key = lambda x: float(x['average_length']), reverse=True)

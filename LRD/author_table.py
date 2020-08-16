from PyQt5.QtWidgets import QTableWidgetItem

from tables.generic_table import GenericTable

class AuthorTable(GenericTable):
	"""
	Table for book authors and their stats.
	
	args:
	get_books: function to be called when an author is selected, in
	order to get a list of books by the selected author.
	
	source_list: list which content will be loaded into table.
	
	attributes:
	self.current_sorting: column selected for sorting table.
	"""
	
	def __init__(self, parent, source_list):
		super().__init__(column_count = 4)
		self.parent = parent
		self.source_list = source_list
		self.current_sorting = '1'
		
		self.itemSelectionChanged.connect(self.parent.get_author)
		self.setHorizontalHeaderLabels((
			"Author",
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
		Calls function to get a list of authors, unless refreshing 
		after sorting, then adds list content to table.
		"""
		
		if not sorting:
			self.parent.get_list_by_attribute()
		self.sort_table(self.current_sorting)
		self.setRowCount(0)
		for entry in self.source_list:
			author = QTableWidgetItem(entry['author'])
			book_count = QTableWidgetItem(str(entry['book_count']))
			average_rating = QTableWidgetItem(entry['average_rating'])
			average_length = QTableWidgetItem(entry['average_length'])
			
			row = self.rowCount()
			self.insertRow(row)
			self.setItem(row, 0, author)
			self.setItem(row, 1, book_count)
			self.setItem(row, 2, average_rating)
			self.setItem(row, 3, average_length)
		
		
	def sort_table(self, mode):
		"""
		Sorts table by selected column/attribute.
		
		args:
		mode: column index and whether reverse order or not.
		"""
		
		if mode == '0r': self.source_list.sort(key = lambda x: f"{x['author'].split()[-1]}, {' '.join(x['author'].split()[0:-1])}" if ',' not in x['author'] else x['author'].lower(), reverse=True)
		elif mode == '0': self.source_list.sort(key = lambda x: f"{x['author'].split()[-1]}, {' '.join(x['author'].split()[0:-1])}" if ',' not in x['author'] else x['author'].lower())
		elif mode == '1r': self.source_list.sort(key = lambda x: x['book_count'])
		elif mode == '1': self.source_list.sort(key = lambda x: x['book_count'], reverse=True)
		elif mode == '2r': self.source_list.sort(key = lambda x: float(x['average_rating']))
		elif mode == '2': self.source_list.sort(key = lambda x: float(x['average_rating']), reverse=True)
		elif mode == '3r': self.source_list.sort(key = lambda x: float(x['average_length']))
		elif mode == '3': self.source_list.sort(key = lambda x: float(x['average_length']), reverse=True)

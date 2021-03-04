from PyQt5.QtWidgets import QTableWidgetItem

from tables.generic_table import GenericTable

class YearReadTable(GenericTable):
	"""
	Table for stats on books read by year. Book count, average rating,
	page count, average pages.
	
	args:
	get_books: function that gets a list of books read in the selected 
	year.
	
	get_year_read: function that gets a list of items which will be 
	shown in this table.
	
	source_list: list that contains the data to be shown in this table.
	"""
	
	def __init__(self, parent, source_list):
		super().__init__(column_count = 5)
		self.parent = parent
		self.source_list = source_list
		self.current_sorting = '0r'
		
		self.itemSelectionChanged.connect(parent.get_year)
		self.setHorizontalHeaderLabels((
			"Year",
			"Books",
			"Average Rating",
			"Total Pages Read",
			"Average Length",
			))
		self.setColumnWidth(0,100)
		self.setColumnWidth(1,50)
		self.setColumnWidth(2,100)
		self.setColumnWidth(3,100)
		self.setColumnWidth(4,100)
		
		
	def refresh_table(self, sorting=False):
		"""
		Gets a list of stats by year or user's reading, except if it's
		refreshing after sorting.
		Adds list content to table.
		"""
		
		if not sorting:
			self.parent.get_list_by_attribute()
		self.sort_table(self.current_sorting)
		self.setRowCount(0)
		for entry in self.source_list:
			year = QTableWidgetItem(entry['year'])
			book_count = QTableWidgetItem(str(entry['book_count']))
			average_rating = QTableWidgetItem(entry['average_rating'])
			total_pages = QTableWidgetItem(entry['total_pages'])
			average_length = QTableWidgetItem(entry['average_length'])
			
			row = self.rowCount()
			self.insertRow(row)
			self.setItem(row, 0, year)
			self.setItem(row, 1, book_count)
			self.setItem(row, 2, average_rating)
			self.setItem(row, 3, total_pages)
			self.setItem(row, 4, average_length)
		
	
	def sort_table(self, mode):
		"""
		Sorts table by selected column/attribute, then calls
		<refresh_table>.
		
		args:
		mode: column index and whether reverse order or not.
		"""
		
		if mode == '0r': self.source_list.sort(key = lambda x: x['year'], reverse=True)
		elif mode == '0': self.source_list.sort(key = lambda x: x['year'])	
		elif mode == '1r': self.source_list.sort(key = lambda x: x['book_count'])
		elif mode == '1': self.source_list.sort(key = lambda x: x['book_count'], reverse=True)
		elif mode == '2r': self.source_list.sort(key = lambda x: float(x['average_rating']), reverse=True)
		elif mode == '2': self.source_list.sort(key = lambda x: float(x['average_rating']))
		elif mode == '3r': self.source_list.sort(key = lambda x: int(x['total_pages']))
		elif mode == '3': self.source_list.sort(key = lambda x: int(x['total_pages']), reverse=True)
		elif mode == '4r': self.source_list.sort(key = lambda x: float(x['average_length']))
		elif mode == '4': self.source_list.sort(key = lambda x: float(x['average_length']), reverse=True)

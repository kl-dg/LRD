from PyQt5.QtWidgets import QTableWidgetItem

from library.queries import get_list_by_attribute
from tables.generic_table import GenericTable


class SeriesTable(GenericTable):
	"""
	Table for a list of serieses or collections and their stats.
	
	args:
	content: either 'series' or 'collection'.
	
	get_books: function to get books by selected series or collection.
	
	source_list: list containing the data which will be loaded into
	this table.
	
	attributes:
	self.current_sorting: column selected for sorting table.
	"""
	
	def __init__(self, parent, content, get_books, source_list):
		super().__init__(column_count = 3)
		self.parent = parent
		self.content = content
		self.get_books = get_books
		self.current_sorting = '0'
		self.source_list = source_list
		
		self.itemSelectionChanged.connect(self.get_books)
		self.clicked.connect(lambda: self.switch_to_this_table(parent.current_table))
		self.setHorizontalHeaderLabels((
			self.content.title(),
			"Books",
			"Average Rating",
			))
		self.setColumnWidth(0,240)
		self.setColumnWidth(1,48)
		self.setColumnWidth(2,95)
		
	
	def switch_to_this_table(self, current_table):
		"""
		This should be run when itemSelectionChanged is not emitted 
		because user clicked on the last selected item from this table
		before selecting an item from the other table.
		"""
		
		if current_table != self.content: self.get_books()
	
		
	def refresh_table(self, sorting=False):
		"""
		Gets a list of series or collection and thir stats, unless 
		refreshing after sorting table. Adds list contents to table.
		"""
		
		if not sorting:
			get_list_by_attribute(self.source_list, self.content)
		self.sort_table(self.current_sorting)
		self.setRowCount(0)
		for entry in self.source_list:
			title = QTableWidgetItem(entry['title'])
			book_count = QTableWidgetItem(str(entry['book_count']))
			average_rating = QTableWidgetItem(entry['average_rating'])
			
			row = self.rowCount()
			self.insertRow(row)
			self.setItem(row, 0, title)
			self.setItem(row, 1, book_count)
			self.setItem(row, 2, average_rating)			

	
	def sort_table(self, mode):
		"""
		Sorts table by selected column/attribute, then calls
		<refresh_table>.
		
		args:
		mode: column index and whether reverse order or not.
		"""
		
		if mode == '0r': self.source_list.sort(key = lambda x: x['title'].lower(), reverse=True)
		elif mode == '0': self.source_list.sort(key = lambda x: x['title'].lower())	
		elif mode == '1r': self.source_list.sort(key = lambda x: x['book_count'], reverse=True)
		elif mode == '1': self.source_list.sort(key = lambda x: x['book_count'])
		elif mode == '2r': self.source_list.sort(key = lambda x: float(x['average_rating']), reverse=True)
		elif mode == '2': self.source_list.sort(key = lambda x: float(x['average_rating']))

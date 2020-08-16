from PyQt5.QtWidgets import QTableWidgetItem

from tables.generic_table import GenericTable


class PublisherTable(GenericTable):
	"""
	Table for book publishers and their stats.
	
	args:
	get_clicked_publisher: function to get selected publisher in order
	to get a list of its books.
	
	source_list: list with contents that'll be added to table.
	
	attributes:
	self.current_sorting: column selected for sorting table.
	"""
	
	def __init__(self, parent, source_list):
		super().__init__(column_count = 3)
		self.parent = parent
		self.source_list = source_list
		self.current_sorting = '1'
		
		self.itemSelectionChanged.connect(parent.get_publisher)
		self.setHorizontalHeaderLabels((
			"Publisher",
			"Books",
			"Average Rating",
			))
		self.setColumnWidth(0,250)
		self.setColumnWidth(1,50)
		self.setColumnWidth(2,100)	
		
		
	def refresh_table(self, sorting=False):
		"""
		Call function to get a list of publishers, unless refreshing 
		after sorting table. Then add list contents to table.
		"""
		
		if not sorting:
			self.parent.get_list_by_attribute(self.source_list, 'publisher')
		self.sort_table(self.current_sorting)
		self.setRowCount(0)
		for entry in self.source_list:
			publisher = QTableWidgetItem(entry['title'])
			book_count = QTableWidgetItem(str(entry['book_count']))
			average_rating = QTableWidgetItem(entry['average_rating'])
			
			row = self.rowCount()
			self.insertRow(row)
			self.setItem(row, 0, publisher)
			self.setItem(row, 1, book_count)
			self.setItem(row, 2, average_rating)
		
	
	def sort_table(self, mode):
		"""
		Sorts table by selected column/attribute.
		
		args:
		mode: column index and whether reverse order or not.
		"""
		
		if mode == '0r': self.source_list.sort(key = lambda x: x['title'].lower(), reverse=True)
		elif mode == '0': self.source_list.sort(key = lambda x: x['title'].lower())	
		elif mode == '1r': self.source_list.sort(key = lambda x: x['book_count'])
		elif mode == '1': self.source_list.sort(key = lambda x: x['book_count'], reverse=True)
		elif mode == '2r': self.source_list.sort(key = lambda x: float(x['average_rating']), reverse=True)
		elif mode == '2': self.source_list.sort(key = lambda x: float(x['average_rating']))

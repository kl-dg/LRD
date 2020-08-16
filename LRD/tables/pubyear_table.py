from PyQt5.QtWidgets import QTableWidgetItem

from library.book_library import year_list
from tables.generic_table import GenericTable

class PubYearTable(GenericTable):
	"""
	Table for stats on books by time span.
	
	args:
	parent: tab reference for using its methods.
	
	attributes:
	self.current_sorting: column selected for sorting table.
	"""
	
	def __init__(self, parent):
		super().__init__(column_count = 3)
		self.parent = parent
		self.current_sorting = '0r'
		
		self.itemSelectionChanged.connect(self.parent.get_year)
		self.setHorizontalHeaderLabels((
			"Year",
			"Books",
			"Average Rating",
			))
		self.setColumnWidth(0,250)
		self.setColumnWidth(1,50)
		self.setColumnWidth(2,100)
		
		
	def refresh_table(self, sorting=False):
		"""
		Gets a list of stats on books' publication years, except if
		sorting, then list contents to table.
		"""
		
		if not sorting:
			self.parent.get_pubyear_list()
		self.sort_table(self.current_sorting)
		self.setRowCount(0)
		for entry in year_list:
			year_label = lambda year: f"{year}s" if 'older' not in year and self.parent.current_time_unit == 'decade' \
				else (f"{int(year)+1}-{int(year)+100}" if 'older' not in year and self.parent.current_time_unit == 'century' \
				else year)
				
			year = QTableWidgetItem(year_label(entry['title']))
			book_count = QTableWidgetItem(str(entry['book_count']))
			average_rating = QTableWidgetItem(entry['average_rating'])
			
			row = self.rowCount()
			self.insertRow(row)
			self.setItem(row, 0, year)
			self.setItem(row, 1, book_count)
			self.setItem(row, 2, average_rating)
		
	
	def sort_table(self, mode):
		"""
		Sorts table by selected column/attribute, then calls
		<refresh_table>.
		
		args:
		mode: column index and whether reverse order or not.
		"""
		
		if mode == '0r': year_list.sort(key = lambda x: x['title'].lower(), reverse=True)
		elif mode == '0': year_list.sort(key = lambda x: x['title'].lower())	
		elif mode == '1r': year_list.sort(key = lambda x: x['book_count'])
		elif mode == '1': year_list.sort(key = lambda x: x['book_count'], reverse=True)
		elif mode == '2r': year_list.sort(key = lambda x: float(x['average_rating']), reverse=True)
		elif mode == '2': year_list.sort(key = lambda x: float(x['average_rating']))

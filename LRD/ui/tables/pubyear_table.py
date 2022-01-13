from PyQt5.QtWidgets import QTableWidgetItem

from data.libraries import years
from control.queries import get_pubyear_list
from ui.tables.generic_table import GenericTable

class PubYearTable(GenericTable):
	"""
	Table for stats on books by time span.
	
	args:
	parent: tab reference for using its methods.
	
	attributes:
	self.current_sorting: column selected for sorting table.
	"""
	
	def __init__(self, parent_tab):
		super().__init__(column_count = 3)
		self.parent_tab = parent_tab
		self.current_sorting = '0r'
		self.selected_year = None
		
		self.itemSelectionChanged.connect(self.year_selection_changed)
		self.setHorizontalHeaderLabels((
			"Year",
			"Books",
			"Average Rating",
			))
		self.setColumnWidth(0,250)
		self.setColumnWidth(1,50)
		self.setColumnWidth(2,100)
		
	
	def get_selected_year(self):
		"""
		Returns label of the selected year if there's a selected year.
		"""
		
		index = [index.row() for index in self.selectionModel().selectedRows()]
		if index:
			return years[index[0]]['title']
			
			
	def year_selection_changed(self):
		"""
		When user selects a different year, record its label on self.selected_year
		and refresh books by year table in order to display all books published on the selected year.
		"""
		
		if self.get_selected_year():
			self.selected_year = self.get_selected_year()	
			self.parent_tab.refresh_books_by_year_table()
		
		
	def refresh_table(self, sorting=False):
		"""
		Gets a list of stats on books' publication years, except if
		sorting, then list contents to table.
		"""
		
		if not sorting:
			get_pubyear_list(self.parent_tab.current_time_unit, self.parent_tab.selected_release_type)
		self.sort_table(self.current_sorting)
		self.setRowCount(0)
		for entry in years:
			#year_label expression will add an "s" to decades. Example: "1920s". While centuries label will be turned
			#into an interval string. Example: "1801-1900".
			year_label = lambda year: f"{year}s" if 'older' not in year and self.parent_tab.current_time_unit == 'decade' \
				else (f"{int(year)+1}-{int(year)+100}" if 'older' not in year and self.parent_tab.current_time_unit == 'century' \
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
		
		if mode == '0r': years.sort(key = lambda x: x['title'].lower(), reverse=True)
		elif mode == '0': years.sort(key = lambda x: x['title'].lower())	
		elif mode == '1r': years.sort(key = lambda x: x['book_count'])
		elif mode == '1': years.sort(key = lambda x: x['book_count'], reverse=True)
		elif mode == '2r': years.sort(key = lambda x: float(x['average_rating']), reverse=True)
		elif mode == '2': years.sort(key = lambda x: float(x['average_rating']))

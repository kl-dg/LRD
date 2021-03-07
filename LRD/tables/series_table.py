from PyQt5.QtWidgets import QTableWidgetItem

from library.book_library import series_list, collection_list
from library.queries import get_list_by_attribute
from tables.generic_table import GenericTable


class SeriesTable(GenericTable):
	"""
	Table for a list of serieses or collections and their stats.
	
	args:
	content: either 'series' or 'collection'.
	
	attributes:
	self.current_sorting: column selected for sorting table.
	"""
	
	def __init__(self, parent_tab, content):
		super().__init__(column_count = 3)
		self.parent_tab = parent_tab
		self.content = content
		self.current_sorting = '0'
		self.selected_item = None
		self.source_list = series_list if content == 'series' else collection_list
		
		self.itemSelectionChanged.connect(self.series_selection_changed)
		self.clicked.connect(lambda: self.switch_to_this_table(parent_tab.current_table))
		self.setHorizontalHeaderLabels((
			self.content.title(),
			"Books",
			"Average Rating",
			))
		self.setColumnWidth(0,240)
		self.setColumnWidth(1,48)
		self.setColumnWidth(2,95)
		
		
	def get_selected_series(self):
		"""
		Returns selected series' or collection's name, if there's a selected one.
		"""
		
		index = [index.row() for index in self.selectionModel().selectedRows()]
		if index:
			if self.content == 'series':
				return series_list[index[0]]['title']
			elif self.content == 'collection':
				return collection_list[index[0]]['title']
				
				
	def series_selection_changed(self):
		"""
		When user selects other series or collection, display all books in that series or collection.
		This is achieved by: getting the selected item and storing it. Informing the window tab of the selection type
		(series or collection) and finally refreshing the books by series or collection table.
		"""
		
		if self.get_selected_series():
			self.selected_item = self.get_selected_series()
			self.parent_tab.current_table = self.content
			self.parent_tab.refresh_books_by_series_table()	
		
	
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

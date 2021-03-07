from PyQt5.QtWidgets import QTableWidgetItem

from library.book_library import author_list
from library.queries import get_list_of_authors
from tables.generic_table import GenericTable

class AuthorTable(GenericTable):
	"""
	Table for book authors and their stats.
	
	args:
	get_books: function to be called when an author is selected, in
	order to get a list of books by the selected author.
	
	attributes:
	self.current_sorting: column selected for sorting table.
	"""
	
	def __init__(self, parent_tab):
		super().__init__(column_count = 4)
		self.parent_tab = parent_tab
		self.selected_author = None
		self.current_sorting = '1'
		
		self.itemSelectionChanged.connect(self.author_selection_changed)
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
		
	
	def get_selected_author(self):
		"""
		Returns name of the selected author if there's a selected author.
		"""
		
		index = [index.row() for index in self.selectionModel().selectedRows()]
		if index:
			return author_list[index[0]]['author']
			
			
	def author_selection_changed(self):
		"""
		When user selects a different author, record its name on self.selected_author
		and refresh books by author table in order to display all books written by this author.
		"""
		
		if self.get_selected_author():
			self.selected_author = self.get_selected_author()	
			self.parent_tab.refresh_books_by_author_table()
			
		
	def refresh_table(self, sorting=False):
		"""
		Calls function to get a list of authors, unless refreshing 
		after sorting, then adds list content to table.
		"""
		
		if not sorting:
			get_list_of_authors()
		self.sort_table(self.current_sorting)
		self.setRowCount(0)
		for entry in author_list:
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
		
		if mode == '0r': author_list.sort(key = lambda x: f"{x['author'].lower().split()[-1]}, {' '.join(x['author'].lower().split()[0:-1])}" if ',' not in x['author'] else x['author'].lower(), reverse=True)
		elif mode == '0': author_list.sort(key = lambda x: f"{x['author'].lower().split()[-1]}, {' '.join(x['author'].lower().split()[0:-1])}" if ',' not in x['author'] else x['author'].lower())
		elif mode == '1r': author_list.sort(key = lambda x: x['book_count'])
		elif mode == '1': author_list.sort(key = lambda x: x['book_count'], reverse=True)
		elif mode == '2r': author_list.sort(key = lambda x: float(x['average_rating']))
		elif mode == '2': author_list.sort(key = lambda x: float(x['average_rating']), reverse=True)
		elif mode == '3r': author_list.sort(key = lambda x: float(x['average_length']))
		elif mode == '3': author_list.sort(key = lambda x: float(x['average_length']), reverse=True)

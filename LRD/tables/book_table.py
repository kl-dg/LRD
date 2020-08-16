from PyQt5.QtWidgets import QTableWidgetItem

from functions.string_formatting import get_int
from library.book_library import book_list
from panel.refresh import refresh_panel
from tables.generic_table import GenericTable



class BookTable(GenericTable):
	"""
	Creates a table for displaying a liat of books.
	
	args:
	parent_tab: main window tab where table is inserted so as to use
	its methods and edit its widgets.
	
	source_list: list of indexes of books that should be displayed in
	the table.
	
	attributes:
	self.current_sorting: column selected for sorting table.
	"""
	
	def __init__(self, parent_tab, source_list):
		super().__init__(column_count = 9)
		self.current_sorting = None
		self.parent_tab = parent_tab
		self.source_list = source_list
		
		self.itemSelectionChanged.connect(self.get_selected_book)
		self.setHorizontalHeaderLabels((
			"Title", 
			"Author", 
			"Pages", 
			"Rating", 
			"Date Read", 
			"Reading Status",
			"Format",
			"Publisher",
			"Publication Year",
			))
		self.setColumnWidth(0,350)
		self.setColumnWidth(1,200)
		self.setColumnWidth(2,50)
		self.setColumnWidth(3,50)
		self.setColumnWidth(4,80)
		self.setColumnWidth(5,100)
		self.setColumnWidth(6,80)
		self.setColumnWidth(7,200)
		self.setColumnWidth(8,100)
		
		
	def refresh_table(self, **args):
		"""
		Removes all books currently on table, then adds all books on
		the refreshed source list.
		"""
		
		self.sort_table(self.current_sorting)
		self.setRowCount(0)
		for index in self.source_list:
			title = QTableWidgetItem(book_list[index].title)
			author = QTableWidgetItem('; '.join(book_list[index].author))
			num_pages = QTableWidgetItem(book_list[index].num_pages)
			rating = QTableWidgetItem(book_list[index].rating)
			date_read = QTableWidgetItem(book_list[index].date_to_ddmmmyyyy('date_read'))
			reading_status = QTableWidgetItem(book_list[index].reading_status)
			format_ = QTableWidgetItem(book_list[index].book_format)
			publisher = QTableWidgetItem(book_list[index].publisher)
			publication_year = QTableWidgetItem(book_list[index].edition_publication_year)
			
			row = self.rowCount()
			self.insertRow(row)
			self.setItem(row, 0, title)
			self.setItem(row, 1, author)
			self.setItem(row, 2, num_pages)
			self.setItem(row, 3, rating)
			self.setItem(row, 4, date_read)
			self.setItem(row, 5, reading_status)
			self.setItem(row, 6, format_)
			self.setItem(row, 7, publisher)
			self.setItem(row, 8, publication_year)
		
		
	def get_selected_book(self):
		"""
		Gets the static library index of selected book then calls
		function to refresh book information panel of the tab where
		the table is in.
		"""
		
		index = [index.row() for index in self.selectionModel().selectedRows()]
		if index:
			self.parent_tab.selected_book = book_list[self.source_list[index[0]]].static_index
			refresh_panel(self.parent_tab)			
		
		
	def sort_table(self, mode):
		"""
		Sorts books table by selected column/attribute.
		
		args:
		mode: column index and whether reverse order or not.
		"""
		
		if mode == '0r': self.source_list.sort(key = lambda x: book_list[x].title.lower(), reverse=True)
		elif mode == '0': self.source_list.sort(key = lambda x: book_list[x].title.lower())	
		elif mode == '1r': self.source_list.sort(key = lambda x: book_list[x].author_sorted().lower(), reverse=True)
		elif mode == '1': self.source_list.sort(key = lambda x: book_list[x].author_sorted().lower())
		elif mode == '2r': self.source_list.sort(key = lambda x: get_int(book_list[x].num_pages), reverse=True)
		elif mode == '2': self.source_list.sort(key = lambda x: get_int(book_list[x].num_pages))
		elif mode == '3r': self.source_list.sort(key = lambda x: get_int(book_list[x].rating))
		elif mode == '3': self.source_list.sort(key = lambda x: get_int(book_list[x].rating), reverse=True)
		elif mode == '4r': self.source_list.sort(key = lambda x: book_list[x].date_sortable('date_read'))
		elif mode == '4': self.source_list.sort(key = lambda x: book_list[x].date_sortable('date_read'), reverse=True)
		elif mode == '5r': self.source_list.sort(key = lambda x: book_list[x].reading_status, reverse=True)
		elif mode == '5': self.source_list.sort(key = lambda x: book_list[x].reading_status)
		elif mode == '6r': self.source_list.sort(key = lambda x: book_list[x].book_format, reverse=True)
		elif mode == '6': self.source_list.sort(key = lambda x: book_list[x].book_format)
		elif mode == '7r': self.source_list.sort(key = lambda x: book_list[x].publisher.lower(), reverse=True)
		elif mode == '7': self.source_list.sort(key = lambda x: book_list[x].publisher.lower())
		elif mode == '8r': self.source_list.sort(key = lambda x: get_int(book_list[x].edition_publication_year), reverse=True)
		elif mode == '8': self.source_list.sort(key = lambda x: get_int(book_list[x].edition_publication_year))
		

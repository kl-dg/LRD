from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout
	
from functions.value_calculations import average
from library.book_library import (
	author_list,
	book_list, 
	books_by_author_list,
	)
from mw_tabs.main_window_tab import GenericMainWindowTab
from panel.refresh import refresh_panel
from panel.empty_panel import EmptyPanel
from tables.author_table import AuthorTable
from tables.book_table import BookTable


class AuthorTab(GenericMainWindowTab):
	"""
	Layout for Author Tab in main window.

	Tab Layout: 
	self.layout: divides screen horizontally, Info Panel on right side,
	author table and books by author table on the left.
	
	self.tables_area: divides the screen vertically, the top for the
	author table and widgets, the bottom half for books by author table.
	
	self.author_table_area: divides the top left horizontally, the left
	side for author table, right side for widgets.
	
	args:
	main_window: parent reference for using its methods.
	
	attributes:
	self.selected_author: last clicked author, whose books will be
	shown in books by author table.
	
	self.run_for_the_first_time: checking used by a layout placeholder.
	
	self.selected_book: last book clicked, for displaying in Info Panel.
	"""
	
	def __init__(self, main_window):
		super().__init__(main_window)
		self.selected_author = None
		self.run_for_the_first_time = True
		self.selected_book = None
		
		self.author_count_info_layout = QHBoxLayout()
		
		self.author_table = AuthorTable(self, author_list)
		self.books_by_author_table = BookTable(self, books_by_author_list)
		
		button_edit_author = QPushButton("Edit selected author")
		button_edit_author.clicked.connect(self.clicked_edit_author)
		
		button_show_no_author = QPushButton("Show books without author")
		button_show_no_author.clicked.connect(self.get_books_without_author)
		
		widgets_area = QVBoxLayout()
		widgets_area.addLayout(self.author_count_info_layout)
		widgets_area.addWidget(button_edit_author)
		widgets_area.addWidget(button_show_no_author)
		
		author_table_area = QHBoxLayout()
		author_table_area.addWidget(self.author_table, 7)
		author_table_area.addLayout(widgets_area, 4)
		
		tables_area = QVBoxLayout()
		tables_area.addLayout(author_table_area)
		tables_area.addWidget(QLabel(f"Books by selected author"))
		tables_area.addWidget(self.books_by_author_table)
		
		self.panel = EmptyPanel()
		
		self.layout = QHBoxLayout(self)
		self.layout.addLayout(tables_area)
		self.layout.addWidget(self.panel)


	def refresh_tab(self):
		"""
		When user comes back to author tab, refresh authors, the book by
		the selected author, the author count widget and book info 
		in Info Panel.
		"""
		if self.is_outdated:
			self.author_table.refresh_table()
			self.get_books_by_author()
			self.refresh_author_count_info()
			refresh_panel(self)
			self.is_outdated = False
		
		
	def reset_selections(self):
		"""
		When user opens other library, reset books by author table
		and Info Panel.
		"""
		
		self.selected_author = None
		self.selected_book = None
		
		
	def refresh_author_count_info(self):
		"""
		Refreshes the message telling the amount of different authors 
		in the library.
		"""
		
		if self.run_for_the_first_time == True:
			self.run_for_the_first_time = False
		else:
			self.author_count_info_layout.removeWidget(self.author_count_info)
			self.author_count_info.deleteLater()
		
		self.author_count_info = QLabel(f"Your library has {len(book_list)} books by {len(author_list)} authors")
		self.author_count_info_layout.addWidget(self.author_count_info)
		
		
	def clicked_edit_author(self):
		"""
		Gets selected author and calls batch edit author name. 
		"""
		
		index = [index.row() for index in self.author_table.selectionModel().selectedRows()]
		if index:
			self.main_window.edit_attribute(author_list[index[0]]['author'], 'author')
			
			
	def get_list_by_attribute(self):
		"""
		Fills author list with unique author names, their book counts,
		average rating and length.
		"""
		
		author_list.clear()
		
		author_set = set()
		for book in book_list:
			if len(book.author) > 1 or book.author[0]:
				for author in book.author:
					author_set.add(author)
					
		author_dict = dict()
		for author in author_set:
			author_dict[author] = [0, 0, 0, 0, 0]
			
		for book in book_list:
			if len(book.author) > 1 or book.author[0]:
				for author in book.author:
					author_dict[author][0] += 1
					if book.rating:
						author_dict[author][1] += int(book.rating)
						author_dict[author][2] += 1
					if book.num_pages:
						author_dict[author][3] += int(book.num_pages)
						author_dict[author][4] += 1
						
		for key, value in author_dict.items():
			author_list.append(dict(
				author = key,
				book_count = value[0],
				average_rating = f"{average(value[1], value[2]):.2f}",
				average_length = f"{average(value[3], value[4]):.2f}",
				))

		
	def get_author(self):
		"""
		Gets selected author and calls <self.get_books_by_author> in 
		order to get a list of their books.
		"""
		
		index = [index.row() for index in self.author_table.selectionModel().selectedRows()]
		if index:
			self.selected_author = author_list[index[0]]['author']
			self.get_books_by_author()
			
			
	def get_books_without_author(self):
		"""
		Display books with empty author attribute on books by author 
		table.
		"""
		
		books_by_author_list.clear()
		self.selected_author = ""
		self.get_books_by_author()
			
			
	def get_books_by_author(self):
		"""
		Gets a list of books by selected author then calls
		<refresh_table> on books by author table.
		"""
		
		books_by_author_list.clear()
		for index_, book in enumerate(book_list):
			if self.selected_author in book.author:
				books_by_author_list.append(index_)
				
		self.books_by_author_table.refresh_table()

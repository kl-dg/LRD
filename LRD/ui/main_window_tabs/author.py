from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


from data.index_lists import books_by_selected_author
from data.libraries import authors, books
from control.queries import get_list_of_books_by_selected_author
from ui.main_window_proxy import main_window
from ui.info_panel.refresh import refresh_panel
from ui.info_panel.empty_panel import EmptyPanel
from ui.tables.author_table import AuthorTable
from ui.tables.book_table import BookTable


class AuthorTab(QWidget):
	"""
	Layout for Author Tab in main window.

	Tab Layout: 
	self.layout: divides screen horizontally, Info Panel on right side,
	author table and books by author table on the left.
	
	self.tables_area: divides the screen vertically, the top for the
	author table and widgets, the bottom half for books by author table.
	
	self.author_table_area: divides the top left horizontally, the left
	side for author table, right side for widgets.

	attributes:
	self.selected_author: last clicked author, whose books will be
	shown in books by author table.
	
	self.run_for_the_first_time: checking used by a layout placeholder.
	
	self.selected_book: last book clicked, for displaying in Info Panel.
	"""
	
	def __init__(self):
		super().__init__()
		self.is_outdated = True
		self.run_for_the_first_time = True
		self.selected_book = None
		
		self.author_count_info = QLabel()
		self.author_count_info.setStyleSheet('font:10pt')
		self.author_count_info.setWordWrap(True)
		self.author_count_info.setAlignment(Qt.AlignCenter)
		
		self.author_count_info_layout = QHBoxLayout()
		self.author_count_info_layout.addWidget(self.author_count_info)
		
		self.author_table = AuthorTable(self)
		self.books_by_author_table = BookTable(self, books_by_selected_author)
		
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
			self.refresh_books_by_author_table()
			self.author_count_info.setText(f"Your library has {len(books)} books by {len(authors)} authors")
			refresh_panel(self)
			self.is_outdated = False
		
		
	def reset_selections(self):
		"""
		When user opens other library, reset books by author table
		and Info Panel.
		"""
		
		self.author_table.selected_author = None
		self.selected_book = None		
		
		
	def clicked_edit_author(self):
		"""
		Gets selected author and calls batch edit author name. 
		"""
		
		if self.author_table.get_selected_author():
			main_window.edit_attribute(self.author_table.get_selected_author(), 'author')
				
			
	def get_books_without_author(self):
		"""
		Display books with empty author attribute on books by author 
		table.
		"""
		
		self.author_table.selected_author = ""
		self.refresh_books_by_author_table()
		
		
	def refresh_books_by_author_table(self):
		"""
		Refreshes list and table of books written by selected author.
		"""
		
		get_list_of_books_by_selected_author(self.author_table.selected_author)
		self.books_by_author_table.refresh_table()

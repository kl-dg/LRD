from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from data.index_lists import books_by_selected_publisher
from control.queries import get_books_by_publisher
from ui.main_window_proxy import main_window
from ui.info_panel.refresh import refresh_panel
from ui.info_panel.empty_panel import EmptyPanel
from ui.tables.book_table import BookTable
from ui.tables.publisher_table import PublisherTable


class PublisherTab(QWidget):
	"""
	Layout for Publisher Tab in main window.
	
	Tab layout:
	self.layout: divides screen horizontally, Info Panel on right side,
	publisher table and books by publisher table on the left.
	
	self.tables_area: divides the screen vertically, top half for
	publishers table and widgets area, while bottom half for books by
	publisher table.
	
	self.publisher_table_area: divides the screen horizontally, left 
	side for publishers table, right side for widgets.
	
	attributes:
	self.selected_publisher: last publisher clicked by user, which books
	will be shown in books by publisher table.
	
	self.selected_book: last book clicked in books by publisher table,
	its full information will shown in Info Panel.
	"""
	
	def __init__(self):
		super().__init__()
		self.is_outdated = True
		self.selected_book = None

		self.publisher_table = PublisherTable(self)
		self.books_by_publisher_table = BookTable(self, books_by_selected_publisher)
		self.panel = EmptyPanel()
		
		button_edit_publisher = QPushButton("Edit selected publisher")
		button_edit_publisher.clicked.connect(self.clicked_edit_publisher)
		
		button_show_no_publisher = QPushButton("Show books without publisher")
		button_show_no_publisher.clicked.connect(self.clicked_get_books_without_publisher)
		
		widgets_area = QVBoxLayout()
		widgets_area.addWidget(button_edit_publisher)
		widgets_area.addWidget(button_show_no_publisher)
		
		publisher_table_area = QHBoxLayout()
		publisher_table_area.addWidget(self.publisher_table, 7)
		publisher_table_area.addLayout(widgets_area, 4)

		tables_area = QVBoxLayout()
		tables_area.addLayout(publisher_table_area)
		tables_area.addWidget(self.books_by_publisher_table)
		
		self.layout = QHBoxLayout(self)
		self.layout.addLayout(tables_area)
		self.layout.addWidget(self.panel)
		
		
	def refresh_tab(self):
		"""
		When user comes back to this tab, refresh publisher and books 
		by publisher tables and selected book's information in Info 
		Panel.
		"""
		
		if self.is_outdated:
			self.publisher_table.refresh_table()
			self.refresh_books_by_publisher_table()
			refresh_panel(self)
			self.is_outdated = False
		
		
	def reset_selections(self):
		"""
		When user opens other library file, reset selected publisher
		and selected book.
		"""
		
		self.publisher_table.selected_publisher = None
		self.selected_book = None
		
		
	def clicked_edit_publisher(self):
		"""
		Batch edit publisher's name.
		Gets publisher's index at publisher's table then send it edit
		attribute batch name editor dialog.
		"""
		
		if self.publisher_table.get_selected_publisher():
			main_window.edit_attribute(self.publisher_table.get_selected_publisher(), 'publisher')
			
			
	def clicked_get_books_without_publisher(self):
		"""
		In order to get a list of books with an empty publisher 
		attribute, set an empty string to selected book and refresh
		list of books by publisher.
		"""
		
		self.publisher_table.selected_publisher = ""
		self.refresh_books_by_publisher_table()
			
			
	def refresh_books_by_publisher_table(self):
		"""
		Calls get_books_by_publisher() in order to get a list of books by the selected publisher
		then refresh the table.
		"""
		
		get_books_by_publisher(self.publisher_table.selected_publisher)
		self.books_by_publisher_table.refresh_table()

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QTabWidget, QVBoxLayout, QWidget
	
from library.book_library import (
	library, 
	books_read_by_year_list, 
	current_reading_list, 
	gave_up_list, 
	wishlist, 
	not_read_list,
	research_books_list, 
	to_read_list, 
	year_read_list, 
	)
from library.queries import get_read_books_by_year, get_read_books_general_statistics, get_reading_status_lists
from main_ui.main_window_proxy import main_window
from panel.refresh import refresh_panel
from panel.empty_panel import EmptyPanel
from tables.book_table import BookTable
from tables.year_read_table import YearReadTable


class ReadingTab(QWidget):
	"""
	Layout for Reading Status tab in main window.
	
	Tab layout:
	self.layout: splits screen in half. Left side for tabs with tables
	by reading status, right side for book information panel.
	
	attributes:
	self.selected_year: selected year in reading stats by year table.
	Books read in selected year will be shown in books read table.
	
	self.selected_book: last selected book by user, for displaying full
	information in Info Panel.
	"""
	
	def __init__(self):
		super().__init__()
		self.is_outdated = True
		self.selected_book = None
		self.run_for_the_first_time = True
		
		self.current_to_read_tab_settings()
		self.read_tab_settings()
		self.wishlist_tab_settings()
		self.not_read_tab_settings()
		
		reading_status_tabs = QTabWidget()
		reading_status_tabs.addTab(self.tab_current, "Books to read and currently reading")
		reading_status_tabs.addTab(self.tab_read, "Books read")
		reading_status_tabs.addTab(self.tab_wishlist, "Wishlist and for research")
		reading_status_tabs.addTab(self.tab_not_read, "Not read or abandoned")
		
		self.panel = EmptyPanel()
		
		self.layout = QHBoxLayout(self)
		self.layout.addWidget(reading_status_tabs)
		self.layout.addWidget(self.panel)
		
		
	def refresh_tab(self):
		"""
		When user comes back to this tab, refresh all tables and 
		selected book's information in Info Panel.
		"""
		
		if self.is_outdated:
			self.refresh_reading_status_lists()
			self.refresh_books_by_year_read_table()
			self.refresh_info_and_stats()
			refresh_panel(self)
			self.is_outdated = False
		
		
	def reset_selections(self):
		"""
		When user opens other library, reset selected year (from reading
		history table) and selected book.
		"""
		
		self.year_read_table.selected_year = None
		self.selected_book = None
		
		
	def refresh_reading_status_lists(self):
		"""
		Refreshes all reading status lists and calls <refresh_table> on
		their respective tables. Exception made to 'Read' table, which 
		is filtered by year.
		"""
		
		get_reading_status_lists()
		
		self.currently_reading_table.refresh_table()
		self.year_read_table.refresh_table()	
		self.to_read_table.refresh_table()
		self.wishlist_table.refresh_table()				
		self.abandoned_books_table.refresh_table()
		self.research_books_table.refresh_table()
		self.books_not_read_table.refresh_table()
		
		
	#"Currently reading" tab
	def current_to_read_tab_settings(self):
		"""
		Layout for Currently Reading tab, under Reading Progress Tab.
		
		Tab layout:
		Currently reading books above, books to read below.
		"""
		
		self.currently_reading_table = BookTable(self, current_reading_list)
		self.to_read_table = BookTable(self, to_read_list)
		
		current_tab_layout = QVBoxLayout()
		current_tab_layout.addWidget(QLabel("Books currently reading:"))
		current_tab_layout.addWidget(self.currently_reading_table, 3)
		current_tab_layout.addWidget(QLabel("Books to read:"))
		current_tab_layout.addWidget(self.to_read_table, 7)
		
		self.tab_current = QWidget()
		self.tab_current.setLayout(current_tab_layout)
		
		
	#"Read" tab
	def read_tab_settings(self):
		"""
		Layout for books read under Reading Progress tab.
		
		Tab layout:
		self.read_tab_layout: divides the screen vertically, top half
		for yearly stats and widgets, bottom half for books read by
		year table.
		"""
		
		self.year_read_table = YearReadTable(self)
		self.books_by_year_read_table = BookTable(self, books_read_by_year_list)
		
		button_reading_graphs = QPushButton("Reading progress in graphs")
		button_reading_graphs.clicked.connect(main_window.open_graphs_window_reading)
		
		button_library_graphs = QPushButton("Your library in graphs")
		button_library_graphs.clicked.connect(main_window.open_graphs_window_library)
		
		self.stats_and_info_layout = QVBoxLayout()
		
		widgets_area = QVBoxLayout()
		widgets_area.addLayout(self.stats_and_info_layout)
		widgets_area.addWidget(button_reading_graphs)
		widgets_area.addWidget(button_library_graphs)
		
		year_read_area = QHBoxLayout()
		year_read_area.addWidget(self.year_read_table)
		year_read_area.addLayout(widgets_area)
		
		read_tab_layout = QVBoxLayout()
		read_tab_layout.addLayout(year_read_area)
		read_tab_layout.addWidget(self.books_by_year_read_table)
		
		self.tab_read = QWidget()
		self.tab_read.setLayout(read_tab_layout)

		
	def refresh_info_and_stats(self):
		"""
		Refreshes information widgets on books read tab.
		"""
		
		if self.run_for_the_first_time:
			self.run_for_the_first_time = False
			
			self.read_books_count_label = QLabel()
			self.read_books_count_label.setAlignment(Qt.AlignCenter)
			self.read_books_count_label.setStyleSheet('font:10pt')
			
			self.pages_read_count_label = QLabel()
			self.pages_read_count_label.setAlignment(Qt.AlignCenter)
			self.pages_read_count_label.setStyleSheet('font:10pt')
			
			self.average_pages_label = QLabel()
			self.average_pages_label.setAlignment(Qt.AlignCenter)
			self.average_pages_label.setStyleSheet('font:10pt')
			
			self.average_rating_label = QLabel()
			self.average_rating_label.setAlignment(Qt.AlignCenter)
			self.average_rating_label.setStyleSheet('font:10pt')
			
			self.stats_and_info_layout.addWidget(self.read_books_count_label)
			self.stats_and_info_layout.addWidget(self.pages_read_count_label)
			self.stats_and_info_layout.addWidget(self.average_pages_label)
			self.stats_and_info_layout.addWidget(self.average_rating_label)
			
		book_count, page_count, avg_length, avg_rating = get_read_books_general_statistics()
			
		self.read_books_count_label.setText(f"Total books read: {book_count}.")
		self.pages_read_count_label.setText(f"Total pages read: {page_count}.")
		self.average_pages_label.setText(f"Average book length: {avg_length:.1f} pages.")
		self.average_rating_label.setText(f"Average rating: {avg_rating:.2f} stars.")
		
	def refresh_books_by_year_read_table(self):
		"""
		Refresh books read by selected year list and table.
		"""
		
		if self.year_read_table.selected_year is not None:
			get_read_books_by_year(self.year_read_table.selected_year)
			self.books_by_year_read_table.refresh_table()
		
		
	#"To read" tab
	def wishlist_tab_settings(self):
		"""
		Layout for Wishlist in reading tab under Reading Progrees tab.
		
		Tab layout:
		Wishlisted books in reading table above, for research below.
		"""
		
		self.wishlist_table = BookTable(self, wishlist)
		self.research_books_table = BookTable(self, research_books_list)
		
		wishlist_tab_layout = QVBoxLayout()
		wishlist_tab_layout.addWidget(QLabel("Wishlist:"))
		wishlist_tab_layout.addWidget(self.wishlist_table)
		wishlist_tab_layout.addWidget(QLabel("Books used for research rather than reading from cover to cover:"))
		wishlist_tab_layout.addWidget(self.research_books_table)
		
		self.tab_wishlist = QWidget()
		self.tab_wishlist.setLayout(wishlist_tab_layout)
		
		
	#"Other" tab
	def not_read_tab_settings(self):
		"""
		Layout for 'not read' reading statuses tables, under Reading
		Progress tab.
		
		Tab Layout: tables for "Abandoned" and "Not read" books.
		"""
		
		self.books_not_read_table = BookTable(self, not_read_list)
		self.abandoned_books_table = BookTable(self, gave_up_list)
		
		not_read_tab_layout = QVBoxLayout()
		not_read_tab_layout.addWidget(QLabel("Books given up before finishing:"))
		not_read_tab_layout.addWidget(self.abandoned_books_table)
		not_read_tab_layout.addWidget(QLabel("Books cataloged without interest in reading:"))
		not_read_tab_layout.addWidget(self.books_not_read_table)
		
		self.tab_not_read = QWidget()
		self.tab_not_read.setLayout(not_read_tab_layout)

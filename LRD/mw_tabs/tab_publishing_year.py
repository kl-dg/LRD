from PyQt5.QtWidgets import QButtonGroup, QHBoxLayout, QLabel, QRadioButton, QVBoxLayout, QWidget

from library.book_library import books_by_year_list
from library.queries import get_books_by_publishing_year
from panel.refresh import refresh_panel
from panel.empty_panel import EmptyPanel
from tables.book_table import BookTable
from tables.pubyear_table import PubYearTable



class PublishingYearTab(QWidget):
	"""
	Layout for Publication Year tab on main window.
	
	Tab layout:
	self.layout: divides the screen horizontally, right side for book
	information panel, left side for tables and widgets.
	
	self.tables_layout: divides the left side vertically, top half for
	years table and widgets, bottom half for books by selected time 
	period table.
	
	self.year_table_layout: divides top left horizontally, left side for
	time period table, right side for options and widgets.
	
	attributes:
	self.selected_release_type: either copy's edition or original
	publication year(first edition), according to user selection.
	Default: original publication year.
	
	self.current_time_unit: stores user's selection on whether
	publication year table should display stats by year, decade or 
	century.
	Default: decade.
	
	self.selected_year: selected time period for displaying books in
	books by year table.
	
	self.selected_book: last book selected by user, which details
	will be shown in Info Panel.
	"""
	
	def __init__(self):
		super().__init__()
		self.is_outdated = True
		self.selected_release_type = 'original_publication_year'
		self.current_time_unit = 'decade'
		self.selected_book = None
		
		button_original = QRadioButton("Original Publication year")
		button_original.clicked.connect(lambda: self.choose_release('original_publication_year'))
		button_original.setChecked(True)
		button_edition = QRadioButton("Edition Publication Year")
		button_edition.clicked.connect(lambda: self.choose_release('edition_publication_year'))
		
		button_year = QRadioButton("Year")
		button_year.clicked.connect(lambda: self.choose_time_unit('year'))
		button_decade = QRadioButton("Decade")
		button_decade.setChecked(True)
		button_decade.clicked.connect(lambda: self.choose_time_unit('decade'))
		button_century = QRadioButton("Century")
		button_century.clicked.connect(lambda: self.choose_time_unit('century'))
		
		release_group = QButtonGroup(self)
		release_group.addButton(button_original)
		release_group.addButton(button_edition)
		
		period_group = QButtonGroup(self)
		period_group.addButton(button_year)
		period_group.addButton(button_decade)
		period_group.addButton(button_century)
		
		self.time_span_table = PubYearTable(self)
		
		options_layout = QVBoxLayout()
		options_layout.addWidget(QLabel("Display by release:"))
		options_layout.addWidget(button_original)
		options_layout.addWidget(button_edition)
		options_layout.addWidget(QLabel("Display books by:"))
		options_layout.addWidget(button_year)
		options_layout.addWidget(button_decade)
		options_layout.addWidget(button_century)

		year_table_layout = QHBoxLayout()
		year_table_layout.addWidget(self.time_span_table)
		year_table_layout.addLayout(options_layout)
		
		self.books_by_year_table = BookTable(self, books_by_year_list)
		
		tables_layout = QVBoxLayout()
		tables_layout.addLayout(year_table_layout)
		tables_layout.addWidget(self.books_by_year_table)
		
		self.panel = EmptyPanel()
		
		self.layout = QHBoxLayout(self)
		self.layout.addLayout(tables_layout)
		self.layout.addWidget(self.panel)
		
		
	def refresh_tab(self):
		"""
		When user comes back to this tab, refresh, time period table
		<year_table>, books b yselected time span and selected book's
		information.
		"""
		
		if self.is_outdated:
			self.time_span_table.refresh_table()
			self.refresh_books_by_year_table()
			refresh_panel(self)
			self.is_outdated = False
		
		
	def reset_selections(self):
		"""
		When user opens other library, reset selected time span and
		book.
		"""
		
		self.selected_year = None
		self.selected_book = None
	
		
	def choose_release(self, release_type):
		"""
		Writes user selection on release type(original/first or current
		edition) to memory then calls <refresh_table> on time span 
		table.
		"""
		
		self.selected_release_type = release_type
		self.time_span_table.refresh_table()	
		
		
	def choose_time_unit(self, time_unit):
		"""
		Writes user selection on time interval(year, decade or century) 
		to memory then calls <refresh_table> on time span table.
		"""
		
		self.current_time_unit = time_unit
		self.time_span_table.refresh_table()	
		
		
	def refresh_books_by_year_table(self):
		"""
		Refreshes list and table for books published during selected time span.
		"""
		
		if self.time_span_table.selected_year is not None:
			get_books_by_publishing_year(self.time_span_table.selected_year, self.current_time_unit, self.selected_release_type)
			self.books_by_year_table.refresh_table()

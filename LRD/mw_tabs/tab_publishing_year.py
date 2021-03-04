from PyQt5.QtWidgets import QButtonGroup, QHBoxLayout, QLabel, QRadioButton, QVBoxLayout, QWidget

from functions.date_formatting import get_now_year
from functions.value_calculations import average
from library.book_library import library, books_by_year_list, year_list
from library.queries import get_list_by_attribute
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
		self.selected_year = None
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
			self.get_books_by_year()
			refresh_panel(self)
			self.is_outdated = False
		
		
	def reset_selections(self):
		"""
		When user opens other library, reset selected time span and
		book.
		"""
		
		self.selected_year = None
		self.selected_book = None
		
		
	def get_pubyear_list(self):
		"""
		Cleans list of stats by time span <year_list> then calls
		method for refreshing the list according to selected time
		interval, year, decade or century.
		"""
		
		if self.current_time_unit == 'year':
			get_list_by_attribute(year_list, self.selected_release_type)
		elif self.current_time_unit == 'decade':
			self.pubyear_table_to_decade()
		elif self.current_time_unit == 'century':
			self.pubyear_table_to_century()
		
		
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
		
	
	def pubyear_table_to_decade(self):
		"""
		Gets a list of decades with at least one book on specified
		release criteria(first or owned edition), amount of books and
		average rating.
		"""
		
		year_list.clear()
		
		year = get_now_year()
		cur_decade = int(f"{str(year)[0:-1]}0")
		decades_dict = dict()
		while cur_decade > int(year) - 209:
			decades_dict[f"{cur_decade}"] = [0, 0, 0]
			cur_decade -= 10
		decades_dict[f"{cur_decade + 9} or older"] = [0, 0, 0]
		
		for book in library.values():
			if getattr(book, self.selected_release_type):
				try:
					decades_dict[f"{getattr(book, self.selected_release_type)[0:-1]}0"][0] += 1
					if book.rating:
						decades_dict[f"{getattr(book, self.selected_release_type)[0:-1]}0"][1] += 1
						decades_dict[f"{getattr(book, self.selected_release_type)[0:-1]}0"][2] += int(book.rating)
				except KeyError:
					decades_dict[f"{cur_decade + 9} or older"][0] += 1
					if book.rating:
						decades_dict[f"{cur_decade + 9} or older"][1] += 1
						decades_dict[f"{cur_decade + 9} or older"][2] += int(book.rating)
						
		for key, value in decades_dict.items():
			if value[0] > 0:
				year_list.append(dict(
					title = key,
					book_count = value[0],
					average_rating = f"{average(value[2], value[1]):.2f}",
					))
					
		
	def pubyear_table_to_century(self):
		"""
		Gets a list of centuries with at least one book on specified
		release criteria(first or owned edition), amount of books and
		average rating.
		"""
		
		year_list.clear()
		
		year = get_now_year()
		cur_century = int(f"{str(year)[0:-2]}00")
		centuries_dict = dict()
		while cur_century > int(year) - 1099:
			centuries_dict[f"{cur_century}"] = [0, 0, 0]
			cur_century -= 100
		centuries_dict[f"{cur_century + 100} or older"] = [0, 0, 0]
		
		for book in library.values():
			if getattr(book, self.selected_release_type):
				try:
					if not int(getattr(book, self.selected_release_type)) % 100 == 0:
						centuries_dict[f"{getattr(book, self.selected_release_type)[0:-2]}00"][0] += 1
						if book.rating:
							centuries_dict[f"{getattr(book, self.selected_release_type)[0:-2]}00"][1] += 1
							centuries_dict[f"{getattr(book, self.selected_release_type)[0:-2]}00"][2] += int(book.rating)
					elif int(getattr(book, self.selected_release_type)) % 100 == 0:
						centuries_dict[f"{int(f'{getattr(book, self.selected_release_type)[0:-2]}00') - 100}"][0] += 1
						if book.rating:
							centuries_dict[f"{int(f'{getattr(book, self.selected_release_type)[0:-2]}00') - 100}"][1] += 1
							centuries_dict[f"{int(f'{getattr(book, self.selected_release_type)[0:-2]}00') - 100}"][2] += int(book.rating)
				except KeyError:
					centuries_dict[f"{cur_century + 100} or older"][0] += 1
					if book.rating:
						centuries_dict[f"{cur_century + 100} or older"][1] += 1
						centuries_dict[f"{cur_century + 100} or older"][2] += int(book.rating)
						
		for key, value in centuries_dict.items():
			if value[0] > 0:
				year_list.append(dict(
					title = key,
					book_count = value[0],
					average_rating = f"{average(value[2], value[1]):.2f}",
					))


	def get_year(self):
		"""
		Gets clicked year/decade/century on table then calls method
		to get a list of books in that time span.
		"""
		
		index = [index.row() for index in self.time_span_table.selectionModel().selectedRows()]
		if index:
			self.selected_year = year_list[index[0]]['title']
			self.get_books_by_year()
			
			
	def get_books_by_year(self):
		"""
		Gets a list of published books by year/decade/century, then
		calls <refresh_table> on books by published year table.
		"""
		
		books_by_year_list.clear()
		if self.selected_year:
			if self.current_time_unit == 'year':
				for index in library:
					if getattr(library[index], self.selected_release_type) == self.selected_year:
						books_by_year_list.append(index)
			
			elif self.current_time_unit == 'decade':
				for index in library:
					if getattr(library[index], self.selected_release_type):
						if 'older' in self.selected_year:
							if int(getattr(library[index], self.selected_release_type)) < int(f'{int(get_now_year()[0:-1]) - 20}0'):
								books_by_year_list.append(index)
						elif int(getattr(library[index], self.selected_release_type)) >= int(self.selected_year) and int(getattr(library[index], self.selected_release_type)) < int(self.selected_year) + 10:
							books_by_year_list.append(index)				
				
			elif self.current_time_unit == 'century':
				for index in library:
					if getattr(library[index], self.selected_release_type):
						if 'older' in self.selected_year:
							if int(getattr(library[index], self.selected_release_type)) <= int(f'{int(get_now_year()[0:-2]) - 10}00'):
								books_by_year_list.append(index)
						elif int(getattr(library[index], self.selected_release_type)) > int(self.selected_year) and int(getattr(library[index], self.selected_release_type)) <= int(self.selected_year) + 100:
							books_by_year_list.append(index)
					
		self.books_by_year_table.refresh_table()

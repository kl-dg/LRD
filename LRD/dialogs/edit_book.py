from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import (
	QFormLayout,
	QHBoxLayout,
	QLabel,
	QLineEdit,
	QMessageBox,
	QPushButton,
	QSpinBox,
	QTabWidget, 
	QTextEdit,
	QVBoxLayout,
	QWidget, 
	)
	
from functions.date_formatting import get_now_time, ddmmyyyy_to_datetime
from functions.isbn import isbn_10_validator, isbn_13_validator
from functions.string_formatting import to_rating_cb					 				 
from library.strings import available_formats, reading_statuses
from library.book_library import library, Book
from library.library_indexer import get_index
from main_ui.main_window_proxy import main_window
from other_ui.cb_constructors import (
	DayDropDown, 
	FormatDropDown, 
	MonthDropDown, 
	RatingDropDown,
	ReadingStatusDropDown, 
	YearDropDown, 
	)

class EditBook(QWidget):
	"""
	Form for adding or editing a book.
	
	Dialog composition: three tabs, buttons OK ("Add"/"Edit") and 
	"Cancel".
	
	First tab: book information.
	Second tab: user's experience with the book.
	Third tab: quotes and notes.
	
	args:
	index: book's index in library. If no index is given, a new book 
	will be added.
	"""
	
	def __init__(self, index=None):
		super().__init__()
		self.resize(650, 500)
		self.index = index
		self.setWindowModality(Qt.ApplicationModal)
		
		self.info_tab = QWidget()
		self.reading = QWidget()
		self.notes = QWidget()
		
		tabs = QTabWidget()	
		tabs.addTab(self.info_tab, "Book Information")
		tabs.addTab(self.reading, "Reading Status and Review")
		tabs.addTab(self.notes, "Quotes and Notes")
		
		edit_book_button = QPushButton(self)
		edit_book_button.clicked.connect(self.edit_book)
		
		edit_book_dialog_layout = QVBoxLayout(self)
		edit_book_dialog_layout.addWidget(tabs)
		edit_book_dialog_layout.addWidget(edit_book_button)
		
		self.information_tab_settings()
		self.reading_tab_settings()
		self.notes_and_quotes_tab_settings()
		
		if self.index is not None:
			self.setWindowTitle("Edit book")
			self.setWindowIcon(QIcon('icons/edit.png'))
			edit_book_button.setText("Save changes")
			self.preview_current_info()
		else:
			self.setWindowTitle("Add book")
			self.setWindowIcon(QIcon('icons/add.png'))
			edit_book_button.setText("Add Book")
		
		
	def information_tab_settings(self):
		"""
		Layout for book information tab.
		"""
		
		int_validator = QIntValidator()
		
		#First line: Title field
		self.title_field = QLineEdit()
		
		#Second line: author and translator
		author_field_label = QLabel("Author:")
		self.author_field = QLineEdit()
		
		translator_field_label = QLabel("Translator:")
		self.translator_field = QLineEdit()
		
		second_line_layout = QHBoxLayout()
		second_line_layout.addWidget(author_field_label)
		second_line_layout.addWidget(self.author_field)
		second_line_layout.addWidget(translator_field_label)
		second_line_layout.addWidget(self.translator_field)
		
		#Third line: pages and isbn
		pages_field_label = QLabel("Number of Pages:")
		self.pages_field = QLineEdit()
		self.pages_field.setValidator(int_validator)
		
		isbn10_label = QLabel("ISBN 10:")
		self.isbn10_field = QLineEdit()
		
		isbn_10_check_button = QPushButton()
		isbn_10_check_button.setText("Check")
		isbn_10_check_button.clicked.connect(self.check_isbn_10)
		
		isbn13_label = QLabel("ISBN 13:")
		self.isbn13_field = QLineEdit()
		self.isbn13_field.setValidator(int_validator)
		
		isbn_13_check_button = QPushButton()
		isbn_13_check_button.setText("Check")
		isbn_13_check_button.clicked.connect(self.check_isbn_13)
		
		third_line_layout = QHBoxLayout()
		third_line_layout.addWidget(pages_field_label)
		third_line_layout.addWidget(self.pages_field, 5)
		third_line_layout.addWidget(isbn10_label)
		third_line_layout.addWidget(self.isbn10_field, 16)
		third_line_layout.addWidget(isbn_10_check_button)
		third_line_layout.addWidget(isbn13_label)
		third_line_layout.addWidget(self.isbn13_field, 20)
		third_line_layout.addWidget(isbn_13_check_button)
		
		#Fourth line: format, publication year, publisher
		format_label = QLabel("Format:")
		self.format_cb = FormatDropDown()
		
		publication_year_label = QLabel("Publication Year:")
		self.publication_year_field = QLineEdit()
		self.publication_year_field.setValidator(int_validator)
		
		publisher_label = QLabel("Publisher:")
		self.publisher_field = QLineEdit()
		
		fourth_line_layout = QHBoxLayout()
		fourth_line_layout.addWidget(format_label)
		fourth_line_layout.addWidget(self.format_cb)
		fourth_line_layout.addWidget(publication_year_label)
		fourth_line_layout.addWidget(self.publication_year_field, 1)
		fourth_line_layout.addWidget(publisher_label)
		fourth_line_layout.addWidget(self.publisher_field, 5)
		
		
		#Fifth line: series, volume, collection, volume
		series_label = QLabel("Series:")
		self.series_field = QLineEdit()
		
		volume_label = QLabel("Volume:")
		self.volume_in_series_field = QLineEdit()
		
		collection_label = QLabel("Collection:")
		self.collection_field = QLineEdit()
		
		col_volume_label = QLabel("Volume:")
		self.volume_in_collection_field = QLineEdit()
		
		fifth_line_layout = QHBoxLayout()
		fifth_line_layout.addWidget(series_label)
		fifth_line_layout.addWidget(self.series_field, 10)
		fifth_line_layout.addWidget(volume_label)
		fifth_line_layout.addWidget(self.volume_in_series_field, 1)
		fifth_line_layout.addWidget(collection_label)
		fifth_line_layout.addWidget(self.collection_field, 10)
		fifth_line_layout.addWidget(col_volume_label)
		fifth_line_layout.addWidget(self.volume_in_collection_field, 1)
		
		#Sixth line: original title, original publication year
		original_title_label = QLabel("Original Title:")
		self.original_title_field = QLineEdit()
		
		same_title_button = QPushButton()
		same_title_button.setText("Same as title")
		same_title_button.clicked.connect(self.set_title_text)
		
		original_publication_year_label = QLabel("Original publication year:")
		self.original_publication_year_field = QLineEdit()
		self.original_publication_year_field.setValidator(int_validator)
		
		sixth_line_layout = QHBoxLayout()
		sixth_line_layout.addWidget(original_title_label)
		sixth_line_layout.addWidget(self.original_title_field, 5)
		sixth_line_layout.addWidget(same_title_button)
		sixth_line_layout.addWidget(original_publication_year_label)
		sixth_line_layout.addWidget(self.original_publication_year_field, 1)
		
		#Seventh line: Number of volumes and bookshelves
		number_of_volumes_label = QLabel("Number of volumes:")
		self.number_of_volumes_sb = QSpinBox()
		
		bookshelves_label = QLabel("Bookshelves:")
		self.bookshelves_field = QLineEdit()
		
		seventh_line_layout = QHBoxLayout()
		seventh_line_layout.addWidget(number_of_volumes_label)
		seventh_line_layout.addWidget(self.number_of_volumes_sb)
		seventh_line_layout.addWidget(bookshelves_label)
		seventh_line_layout.addWidget(self.bookshelves_field)
		
		#Eighth line: date bought and from where
		date_bought_label = QLabel("Date bought:")
		self.day_bought = DayDropDown()
		self.month_bought = MonthDropDown()
		self.year_bought = YearDropDown()
		
		bought_from_label = QLabel("Bought from:")
		self.bought_from_field = QLineEdit()
		
		eighth_line_layout = QHBoxLayout()
		eighth_line_layout.addWidget(date_bought_label)
		eighth_line_layout.addWidget(self.day_bought)
		eighth_line_layout.addWidget(self.month_bought)
		eighth_line_layout.addWidget(self.year_bought)
		eighth_line_layout.addWidget(bought_from_label)
		eighth_line_layout.addWidget(self.bought_from_field)
		
		#Ninth line: condition
		condition_label = QLabel("My copy's condition:")
		self.condition_field = QLineEdit()

		ninth_line_layout = QHBoxLayout()
		ninth_line_layout.addWidget(condition_label)
		ninth_line_layout.addWidget(self.condition_field)
		
		#Tenth line: weblink
		weblink_label = QLabel("Weblink:")
		self.weblink_field = QLineEdit()
		
		tenth_line_layout = QHBoxLayout()
		tenth_line_layout.addWidget(weblink_label)
		tenth_line_layout.addWidget(self.weblink_field)
		
		#Eleventh line: date added
		if self.index is not None: date_added_label = QLabel(f"Date added: {library[self.index].get_date_as_string('date_added', '%d/%b/%Y %H:%M')}.")
		
		layout = QFormLayout()
		layout.addRow(QLabel("Title:"),self.title_field)
		layout.addRow(second_line_layout)
		layout.addRow(third_line_layout)
		layout.addRow(fourth_line_layout)
		layout.addRow(fifth_line_layout)
		layout.addRow(sixth_line_layout)
		layout.addRow(seventh_line_layout)
		layout.addRow(eighth_line_layout)
		layout.addRow(ninth_line_layout)
		layout.addRow(tenth_line_layout)
		if self.index is not None: layout.addRow(date_added_label)
		layout.setSpacing(10)
		
		self.info_tab.setLayout(layout)
		
		
	def reading_tab_settings(self):
		"""
		Layout for reading status tab.
		"""
		
		
		#First line: date started and date finished
		date_started_label = QLabel("Date started:")
		self.day_started = DayDropDown()
		self.month_started = MonthDropDown()
		self.year_started = YearDropDown()
		
		set_started_today = QPushButton()
		set_started_today.setText("Set to today")
		set_started_today.clicked.connect(self.set_started_today)
		
		date_read_label = QLabel("Date read:")
		self.day_read = DayDropDown()
		self.month_read = MonthDropDown()
		self.year_read = YearDropDown()
		
		set_read_today = QPushButton()
		set_read_today.setText("Set to today")
		set_read_today.clicked.connect(self.set_read_today)
		
		first_line_layout = QHBoxLayout()
		first_line_layout.addWidget(date_started_label)
		first_line_layout.addWidget(self.day_started)
		first_line_layout.addWidget(self.month_started)
		first_line_layout.addWidget(self.year_started)
		first_line_layout.addWidget(set_started_today)
		first_line_layout.addStretch()
		first_line_layout.addWidget(date_read_label)
		first_line_layout.addWidget(self.day_read)
		first_line_layout.addWidget(self.month_read)
		first_line_layout.addWidget(self.year_read)
		first_line_layout.addWidget(set_read_today)
		
		#Second line: reading status, rating, times read
		reading_status_label = QLabel("Reading status:")
		self.reading_status_cb = ReadingStatusDropDown()

		rating_label = QLabel("Rating:")
		self.rating_cb = RatingDropDown()

		times_read_label = QLabel("Times read:")
		self.times_read_sb = QSpinBox()
		
		second_line_layout = QHBoxLayout()
		second_line_layout.addWidget(reading_status_label)
		second_line_layout.addWidget(self.reading_status_cb)
		second_line_layout.addStretch()
		second_line_layout.addWidget(rating_label)
		second_line_layout.addWidget(self.rating_cb)
		second_line_layout.addStretch()
		second_line_layout.addWidget(times_read_label)
		second_line_layout.addWidget(self.times_read_sb)
		
		#Third line and on: review text box
		review_label = QLabel("Review:")
		self.review_box = QTextEdit()
		
		layout = QVBoxLayout()
		layout.addLayout(first_line_layout)
		layout.addLayout(second_line_layout)
		layout.addWidget(review_label)
		layout.addWidget(self.review_box)
		
		self.reading.setLayout(layout)
		
		
	def notes_and_quotes_tab_settings(self):
		"""
		Layout for notes and quotes tab.
		"""
		
		quote_label = QLabel("Quotes:")
		self.quote_box = QTextEdit()
		notes_label = QLabel("Notes:")
		self.notes_box = QTextEdit()
		
		layout = QVBoxLayout()
		layout.addWidget(quote_label)
		layout.addWidget(self.quote_box)
		layout.addWidget(notes_label)
		layout.addWidget(self.notes_box)
		
		self.notes.setLayout(layout)
		
		
	def preview_current_info(self):
		"""
		Fills all available fields when editing a book.
		"""
		
		self.title_field.setText(library[self.index].title)
		self.author_field.setText("; ".join(library[self.index].author))
		self.translator_field.setText(library[self.index].translator)
		self.pages_field.setText(library[self.index].num_pages)
		self.isbn10_field.setText(library[self.index].isbn10)
		self.isbn13_field.setText(library[self.index].isbn13)
		self.format_cb.setCurrentIndex(self.format_cb.findText(self.to_format_cb(library[self.index].book_format)))
		self.publication_year_field.setText(library[self.index].edition_publication_year)
		self.publisher_field.setText(library[self.index].publisher)
		self.series_field.setText(library[self.index].series)
		self.volume_in_series_field.setText(library[self.index].volume_in_series)
		self.collection_field.setText(library[self.index].collection)
		self.volume_in_collection_field.setText(library[self.index].volume_in_collection)
		self.original_title_field.setText(library[self.index].original_title)
		self.original_publication_year_field.setText(library[self.index].original_publication_year)
		self.number_of_volumes_sb.setValue(self.set_number_of_volumes(library[self.index].number_of_volumes))
		self.bookshelves_field.setText("; ".join(library[self.index].bookshelves))
		self.day_bought.setCurrentIndex(library[self.index].date_bought.day if library[self.index].date_bought else 0)
		self.month_bought.setCurrentIndex(library[self.index].date_bought.month if library[self.index].date_bought else 0)
		self.year_bought.setCurrentIndex(self.year_bought.findText(str(library[self.index].date_bought.year)) if library[self.index].date_bought else 0)
		self.condition_field.setText(library[self.index].condition)
		self.weblink_field.setText(library[self.index].weblink)
		self.day_started.setCurrentIndex(library[self.index].date_started.day if library[self.index].date_started else 0)
		self.month_started.setCurrentIndex(library[self.index].date_started.month if library[self.index].date_started else 0)
		self.year_started.setCurrentIndex(self.year_started.findText(str(library[self.index].date_started.year)) if library[self.index].date_started else 0)
		self.day_read.setCurrentIndex(library[self.index].date_read.day if library[self.index].date_read else 0)
		self.month_read.setCurrentIndex(library[self.index].date_read.month if library[self.index].date_read else 0)
		self.year_read.setCurrentIndex(self.year_read.findText(str(library[self.index].date_read.year)) if library[self.index].date_read else 0)
		self.reading_status_cb.setCurrentIndex(self.reading_status_cb.findText(self.to_reading_status_cb(library[self.index].reading_status)))
		self.rating_cb.setCurrentIndex(self.rating_cb.findText(to_rating_cb(library[self.index].rating)))
		self.times_read_sb.setValue(self.set_times_read_sb(library[self.index].times_read))
		self.review_box.setText(library[self.index].review)
		self.quote_box.setText(library[self.index].quotes)
		self.notes_box.setText(library[self.index].notes)
		
		
	def check_isbn_10(self):
		"""
		Checks if the value in the ISBN-10 field is valid and displays
		the result to user.
		"""
		
		if isbn_10_validator(self.isbn10_field.text()):
			QMessageBox.information(self, "Check ISBN-10", 
				"This is a valid ISBN-10 number.", 
				QMessageBox.Ok)
		else:
			QMessageBox.warning(self, "Check ISBN-10", 
				"This is not a valid ISBN-10 number.", 
				QMessageBox.Ok)
		
		
	def check_isbn_13(self):
		"""
		Checks if the value in the ISBN-13 field is valid and displays
		the result to user.
		"""
		
		if isbn_13_validator(self.isbn13_field.text()):
			QMessageBox.information(self, "Check ISBN-13", 
				"This is a valid ISBN-13 number.", 
				QMessageBox.Ok)
		else:
			QMessageBox.warning(self, "Check ISBN-13", 
				"This is not a valid ISBN-13 number.", 
				QMessageBox.Ok)
				
				
	def set_started_today(self):
		"""
		Sets date started reading field to current day.
		"""
		
		self.day_started.setCurrentIndex(get_now_time().day)
		self.month_started.setCurrentIndex(get_now_time().month)
		self.year_started.setCurrentIndex(self.year_started.findText(str(get_now_time().year)))
		
		
	def set_read_today(self):
		"""
		Sets date finished reading field to current day.
		"""
		
		self.day_read.setCurrentIndex(get_now_time().day)
		self.month_read.setCurrentIndex(get_now_time().month)
		self.year_read.setCurrentIndex(self.year_read.findText(str(get_now_time().year)))
				
	
	def to_format_cb(self, value):
		"""
		Integrity check. Checks if <book_format> attribute is an
		available option. If not, return 'Unspecified'.
		"""
		
		if value in available_formats:
			return value
		else:
			return "Unspecified"
			
			
	def to_reading_status_cb(self, value):
		"""
		Integrity check. Checks if <reading_status> attribute is an
		available option. If not, return 'Not read'.
		"""
		   
		if value in reading_statuses:
			return value
		else:
			return "Not read"
			
			
	def set_number_of_volumes(self, value):
		"""
		Integrity check: check if there's a valid integer in
		<number_of_volumes> attribute. If empty or invalid, return 1.
		"""
		   
		try:
			if value: return int(value)
			else: return 1
			
		except ValueError:
			return 1
			
		
	def set_times_read_sb(self, value):
		"""
		Integrity check: check if there's a valid integer in
		<times_read> attribute. If empty or invalid, return 0.
		"""
		   
		try:
			if value: return int(value)
			else: return 0
			
		except ValueError:
			return 0
			
	
	def set_title_text(self):
		"""
		Sets original title field same as title field on button click, 
		if there's a title.
		"""
		   
		if self.title_field.text():
			self.original_title_field.setText(self.title_field.text())
			
			
	def set_rating(self, value):
		"""
		Turns value in rating combobox into a one-digit number.
		"""
		
		if value == "Not rated": return ""
		elif "star" in value: return value[0]
	
	
	def check_int(self, value):
		"""
		QIntValidator lets a few special characters pass, this check
		will prevent ValueError exception later
		"""
			
		try:
			int(value)
			return value
		except ValueError:
			return ""
				
		
	def edit_book(self):
		"""
		If an index was given, changes attributes in currently 
		selected book. Else, add a new book.
		"""
		
		if self.index is not None:
			library[self.index] = Book(
				self.title_field.text().strip(), 
				[item.strip() for item in self.author_field.text().split(';') if len(item.strip()) > 0],
				self.check_int(self.pages_field.text()),
				self.publisher_field.text(),
				self.set_rating(self.rating_cb.currentText()),
				ddmmyyyy_to_datetime(f"{self.day_read.currentText()}/{self.month_read.currentIndex()}/{self.year_read.currentText()}"),
				self.isbn10_field.text(),
				self.isbn13_field.text(),
				library[self.index].date_added,
				ddmmyyyy_to_datetime(f"{self.day_started.currentText()}/{self.month_started.currentIndex()}/{self.year_started.currentText()}"),
				self.reading_status_cb.currentText(),
				self.format_cb.currentText(),
				self.review_box.toPlainText(),
				self.check_int(self.publication_year_field.text()),
				self.check_int(self.original_publication_year_field.text()),
				self.original_title_field.text(),
				self.series_field.text(),
				self.volume_in_series_field.text(),
				self.collection_field.text(),
				self.volume_in_collection_field.text(),
				self.times_read_sb.value(),
				self.number_of_volumes_sb.value(),
				self.translator_field.text(),
				self.weblink_field.text(),
				self.bought_from_field.text(),
				ddmmyyyy_to_datetime(f"{self.day_bought.currentText()}/{self.month_bought.currentIndex()}/{self.year_bought.currentText()}"),
				[item.strip() for item in self.bookshelves_field.text().split(';') if len(item.strip()) > 0],
				self.condition_field.text(),
				self.quote_box.toPlainText(),
				self.notes_box.toPlainText(),
				)
									 
									 
		else:
			library[get_index()] = Book(
				self.title_field.text().strip(), 
				[item.strip() for item in self.author_field.text().split(';') if len(item.strip()) > 0],
				self.check_int(self.pages_field.text()),
				self.publisher_field.text(),
				self.set_rating(self.rating_cb.currentText()),
				ddmmyyyy_to_datetime(f"{self.day_read.currentText()}/{self.month_read.currentIndex()}/{self.year_read.currentText()}"),
				self.isbn10_field.text(),
				self.isbn13_field.text(),
				get_now_time(),
				ddmmyyyy_to_datetime(f"{self.day_started.currentText()}/{self.month_started.currentIndex()}/{self.year_started.currentText()}"),
				self.reading_status_cb.currentText(),
				self.format_cb.currentText(),
				self.review_box.toPlainText(),
				self.check_int(self.publication_year_field.text()),
				self.check_int(self.original_publication_year_field.text()),
				self.original_title_field.text(),
				self.series_field.text(),
				self.volume_in_series_field.text(),
				self.collection_field.text(),
				self.volume_in_collection_field.text(),
				self.times_read_sb.value(),
				self.number_of_volumes_sb.value(),
				self.translator_field.text(),
				self.weblink_field.text(),
				self.bought_from_field.text(),
				ddmmyyyy_to_datetime(f"{self.day_bought.currentText()}/{self.month_bought.currentIndex()}/{self.year_bought.currentText()}"),
				[item.strip() for item in self.bookshelves_field.text().split(';') if len(item.strip()) > 0],
				self.condition_field.text(),
				self.quote_box.toPlainText(),
				self.notes_box.toPlainText(),
				)
								 
		main_window.flag_unsaved_changes = True
		main_window.set_interface_outdated()
		main_window.refresh_current_tab()
		self.close()


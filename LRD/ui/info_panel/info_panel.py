from PyQt5.QtWidgets import QFormLayout, QLabel, QHBoxLayout, QPushButton

from functions.string_formatting import to_rating_cb, get_int
from data.libraries import books
from ui.main_window_proxy import main_window
									  

class InfoPanel(QFormLayout):
	"""
	Layout settings for book's information panel.
	
	args:
	index: selected book's library index.
	
	main_window: referenced in order to use its methods.
	"""
	
	
	def __init__(self, index):
		super().__init__()
		self.setSpacing(10)

		book = books[index]
		
		#Title
		if book.title:
			title_form = QLabel(book.title)
			title_form.setWordWrap(True)
			title_form.setStyleSheet("font: 12pt")
			self.addRow(title_form)
		
		#Series
		if book.series:
			series_str = f"<i>{book.series}</i>"
			if book.volume_in_series:
				series_str = f"{series_str} #{book.volume_in_series}"
			series_form = QLabel(series_str)
			series_form.setStyleSheet('font: 10pt')
			self.addRow(series_form)
			
		#Author
		if len(book.author) > 0:
			self.addRow(QLabel(f"<b>Author:</b> {'; '.join(book.author)}", wordWrap=True))
		
		#Translator
		if book.translator:
			self.addRow(QLabel(f"<b>Translator:</b> {book.translator}"))
			
		#Page count and format
		if book.num_pages or book.book_format or int(get_int(book.number_of_volumes)) > 1: 
			page_and_format_line = QHBoxLayout()
			if book.num_pages:
				page_and_format_line.addWidget(QLabel(f"<b>Length:</b> {book.num_pages} pages"))
			if book.book_format or int(get_int(book.number_of_volumes)) > 1:
				format_str = "<b>Format:</b>"
				if book.book_format:
					format_str = f"{format_str} {book.book_format}"
					if int(get_int(book.number_of_volumes)) > 1:
						format_str = f"{format_str}, {book.number_of_volumes} volumes"
				elif not book.book_format and int(get_int(book.number_of_volumes)) > 1:
					format_str = f"{format_str} {book.number_of_volumes} volumes"
				page_and_format_line.addWidget(QLabel(format_str))
			self.addRow(page_and_format_line)
			
		#Publisher and year publisher
		if book.publisher or book.edition_publication_year:
			publisher_line = QHBoxLayout()
			if book.publisher:
				publisher_line.addWidget(QLabel(f"<b>Published by:</b> {book.publisher}"))
			if book.edition_publication_year:
				publisher_line.addWidget(QLabel(f"<b>Publication year:</b> {book.edition_publication_year}"))
			self.addRow(publisher_line)

		#ISBN
		if book.isbn10 or book.isbn13:
			isbn_line = QHBoxLayout()
			if book.isbn10:
				isbn_line.addWidget(QLabel(f"<b>ISBN-10</b>: {book.isbn10}"))
			if book.isbn13:
				isbn_line.addWidget(QLabel(f"<b>ISBN-13</b>: {book.isbn13}"))
			self.addRow(isbn_line)
			
		#Collection
		if book.collection:
			collection_str = book.collection
			if book.volume_in_collection:
				collection_str = f"{collection_str} #{book.volume_in_collection}"
			self.addRow(QLabel(collection_str))
			
		#Original title
		if book.original_title:
			self.addRow(QLabel(f"<b>Original title:</b> {book.original_title}"))
			
		#Original publication year:
		if book.original_publication_year:
			self.addRow(QLabel(f"<b>Original publication year:</b> {book.original_publication_year}"))
			
		if book.weblink:
			weblink_form = QLabel(f'<b>Weblink:</b> <a href={book.weblink}>Open in browser</a>')
			weblink_form.setOpenExternalLinks(True)
			self.addRow(weblink_form)
			
		#Reading status header
		reading_status_header = QLabel("My reading status")
		reading_status_header.setStyleSheet('font: 11pt')
		self.addRow(reading_status_header)
		
		#Reading status and counter
		reading_line = QHBoxLayout()
		reading_line.addWidget(QLabel(f"<b>Reading status</b>: {book.reading_status}"))
		reading_line.addWidget(QLabel(f"<b>Read counter:</b> {book.times_read}"))
		self.addRow(reading_line)
		
		#Dates started and read
		if book.date_read or book.date_started:
			dates_line = QHBoxLayout()
			if book.date_read:
				dates_line.addWidget(QLabel(f"<b>Date read:</b> {book.get_date_as_string('date_read', '%d/%b/%Y')}"))
			if book.date_started:
				dates_line.addWidget(QLabel(f"<b>Date started:</b> {book.get_date_as_string('date_started', '%d/%b/%Y')}"))
			self.addRow(dates_line)
						
		#Rating and date added
		rating_line = QHBoxLayout()
		if book.rating:
			rating_line.addWidget(QLabel(f"<b>Rating:</b> {to_rating_cb(book.rating)}"))
		rating_line.addWidget(QLabel(f"<b>Date added:</b> {book.get_date_as_string('date_added', '%d/%b/%Y %H:%M')}"))
		self.addRow(rating_line)
			
		#bookshelves
		if len(book.bookshelves) > 0:
			self.addRow(QLabel(f"<b>Bookshelves:</b> {'; '.join(book.bookshelves)}", wordWrap=True))
				
		#Review
		if book.review:
			self.addRow(QLabel(f"<b>Review:</b> {book.review[0:64]}..."))
			
		edit_review_button = QPushButton()
		if book.review:
			edit_review_button.setText("Edit / Read Full Review")
		else:
			edit_review_button.setText("Add Review")
		edit_review_button.clicked.connect(lambda: main_window.get_quick_text_editor("review", index))
		self.addRow(edit_review_button)
		
		#Quotes
		edit_quotes_button = QPushButton()
		if book.quotes:
			edit_quotes_button.setText("Edit / Read All Quotes")
		else:
			edit_quotes_button.setText("Add Quotes")
		edit_quotes_button.clicked.connect(lambda: main_window.get_quick_text_editor("quotes", index))
		self.addRow(edit_quotes_button)
		
		#Notes
		edit_notes_button = QPushButton()
		if book.notes:
			edit_notes_button.setText("Edit / Read All Notes")
		else:
			edit_notes_button.setText("Add Notes")
		edit_notes_button.clicked.connect(lambda: main_window.get_quick_text_editor("notes", index))
		self.addRow(edit_notes_button)
		
		#User's copy header
		copy_header = QLabel("My copy")
		copy_header.setStyleSheet('font: 11pt')
		self.addRow(copy_header)
		if not book.bought_where \
				and not book.date_bought \
				and not book.condition:
			self.addRow(QLabel("(no details)"))

			
		if book.bought_where:
			self.addRow(QLabel(f"<b>Bought at:</b> {book.bought_where}"))
		if book.date_bought:
			self.addRow(QLabel(f"<b>Date bought:</b> {book.get_date_as_string('date_bought', '%d/%b/%Y')}"))
		if book.condition:
			self.addRow(QLabel(f"<b>Condition:</b> {book.condition}"))

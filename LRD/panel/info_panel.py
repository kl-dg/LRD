from PyQt5.QtWidgets import QFormLayout, QLabel, QHBoxLayout, QPushButton

from functions.string_formatting import to_rating_cb, get_int
from library.book_library import library
from main_ui.main_window_proxy import main_window
									  

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
		
		#Title
		if library[index].title:
			title_form = QLabel(library[index].title)
			title_form.setWordWrap(True)
			title_form.setStyleSheet("font: 12pt")
			self.addRow(title_form)
		
		#Series
		if library[index].series:
			series_str = f"<i>{library[index].series}</i>"
			if library[index].volume_in_series:
				series_str = f"{series_str} #{library[index].volume_in_series}"
			series_form = QLabel(series_str)
			series_form.setStyleSheet('font: 10pt')
			self.addRow(series_form)
			
		#Author
		if len(library[index].author) > 0:
			self.addRow(QLabel(f"<b>Author:</b> {'; '.join(library[index].author)}", wordWrap=True))
		
		#Translator
		if library[index].translator:
			self.addRow(QLabel(f"<b>Translator:</b> {library[index].translator}"))
			
		#Page count and format
		if library[index].num_pages or library[index].book_format or int(get_int(library[index].number_of_volumes)) > 1: 
			page_and_format_line = QHBoxLayout()
			if library[index].num_pages:
				page_and_format_line.addWidget(QLabel(f"<b>Length:</b> {library[index].num_pages} pages"))
			if library[index].book_format or int(get_int(library[index].number_of_volumes)) > 1:
				format_str = "<b>Format:</b>"
				if library[index].book_format:
					format_str = f"{format_str} {library[index].book_format}"
					if int(get_int(library[index].number_of_volumes)) > 1:
						format_str = f"{format_str}, {library[index].number_of_volumes} volumes"
				elif not library[index].book_format and int(get_int(library[index].number_of_volumes)) > 1:
					format_str = f"{format_str} {library[index].number_of_volumes} volumes"
				page_and_format_line.addWidget(QLabel(format_str))
			self.addRow(page_and_format_line)
			
		#Publisher and year publisher
		if library[index].publisher or library[index].edition_publication_year:
			publisher_line = QHBoxLayout()
			if library[index].publisher:
				publisher_line.addWidget(QLabel(f"<b>Published by:</b> {library[index].publisher}"))
			if library[index].edition_publication_year:
				publisher_line.addWidget(QLabel(f"<b>Publication year:</b> {library[index].edition_publication_year}"))
			self.addRow(publisher_line)

		#ISBN
		if library[index].isbn10 or library[index].isbn13:
			isbn_line = QHBoxLayout()
			if library[index].isbn10:
				isbn_line.addWidget(QLabel(f"<b>ISBN-10</b>: {library[index].isbn10}"))
			if library[index].isbn13:
				isbn_line.addWidget(QLabel(f"<b>ISBN-13</b>: {library[index].isbn13}"))
			self.addRow(isbn_line)
			
		#Collection
		if library[index].collection:
			collection_str = library[index].collection
			if library[index].volume_in_collection:
				collection_str = f"{collection_str} #{library[index].volume_in_collection}"
			self.addRow(QLabel(collection_str))
			
		#Original title
		if library[index].original_title:
			self.addRow(QLabel(f"<b>Original title:</b> {library[index].original_title}"))
			
		#Original publication year:
		if library[index].original_publication_year:
			self.addRow(QLabel(f"<b>Original publication year:</b> {library[index].original_publication_year}"))
			
		if library[index].weblink:
			weblink_form = QLabel(f'<b>Weblink:</b> <a href={library[index].weblink}>Open in browser</a>')
			weblink_form.setOpenExternalLinks(True)
			self.addRow(weblink_form)
			
		#Reading status header
		reading_status_header = QLabel("My reading status")
		reading_status_header.setStyleSheet('font: 11pt')
		self.addRow(reading_status_header)
		
		#Reading status and counter
		reading_line = QHBoxLayout()
		reading_line.addWidget(QLabel(f"<b>Reading status</b>: {library[index].reading_status}"))
		reading_line.addWidget(QLabel(f"<b>Read counter:</b> {library[index].times_read}"))
		self.addRow(reading_line)
		
		#Dates started and read
		if library[index].date_read or library[index].date_started:
			dates_line = QHBoxLayout()
			if library[index].date_read:
				dates_line.addWidget(QLabel(f"<b>Date read:</b> {library[index].get_date_as_string('date_read', '%d/%b/%Y')}"))
			if library[index].date_started:
				dates_line.addWidget(QLabel(f"<b>Date started:</b> {library[index].get_date_as_string('date_started', '%d/%b/%Y')}"))
			self.addRow(dates_line)
						
		#Rating and date added
		rating_line = QHBoxLayout()
		if library[index].rating:
			rating_line.addWidget(QLabel(f"<b>Rating:</b> {to_rating_cb(library[index].rating)}"))
		rating_line.addWidget(QLabel(f"<b>Date added:</b> {library[index].get_date_as_string('date_added', '%d/%b/%Y %H:%M')}"))
		self.addRow(rating_line)
			
		#bookshelves
		if len(library[index].bookshelves) > 0:
			self.addRow(QLabel(f"<b>Bookshelves:</b> {'; '.join(library[index].bookshelves)}", wordWrap=True))
				
		#Review
		if library[index].review:
			self.addRow(QLabel(f"<b>Review:</b> {library[index].review[0:64]}..."))
			
		edit_review_button = QPushButton()
		if library[index].review:
			edit_review_button.setText("Edit / Read Full Review")
		else:
			edit_review_button.setText("Add Review")
		edit_review_button.clicked.connect(lambda: main_window.get_quick_text_editor("review", index))
		self.addRow(edit_review_button)
		
		#Quotes
		edit_quotes_button = QPushButton()
		if library[index].quotes:
			edit_quotes_button.setText("Edit / Read All Quotes")
		else:
			edit_quotes_button.setText("Add Quotes")
		edit_quotes_button.clicked.connect(lambda: main_window.get_quick_text_editor("quotes", index))
		self.addRow(edit_quotes_button)
		
		#Notes
		edit_notes_button = QPushButton()
		if library[index].notes:
			edit_notes_button.setText("Edit / Read All Notes")
		else:
			edit_notes_button.setText("Add Notes")
		edit_notes_button.clicked.connect(lambda: main_window.get_quick_text_editor("notes", index))
		self.addRow(edit_notes_button)
		
		#User's copy header
		copy_header = QLabel("My copy")
		copy_header.setStyleSheet('font: 11pt')
		self.addRow(copy_header)
		if not library[index].bought_where \
				and not library[index].date_bought \
				and not library[index].condition:
			self.addRow(QLabel("(no details)"))

			
		if library[index].bought_where:
			self.addRow(QLabel(f"<b>Bought at:</b> {library[index].bought_where}"))
		if library[index].date_bought:
			self.addRow(QLabel(f"<b>Date bought:</b> {library[index].get_date_as_string('date_bought', '%d/%b/%Y')}"))
		if library[index].condition:
			self.addRow(QLabel(f"<b>Condition:</b> {library[index].condition}"))

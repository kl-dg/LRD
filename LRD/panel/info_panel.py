from PyQt5.QtWidgets import QFormLayout, QLabel, QHBoxLayout, QPushButton

from functions.string_formatting import to_rating_cb, get_int
from library.book_library import book_list
									  

class InfoPanel(QFormLayout):
	"""
	Layout settings for book's information panel.
	
	args:
	index: selected book's static library index.
	
	main_window: referenced in order to use its methods.
	"""
	
	
	def __init__(self, index, main_window):
		super().__init__()
		self.setSpacing(10)
		
		#Title
		if book_list[index].title:
			title_form = QLabel(book_list[index].title)
			title_form.setWordWrap(True)
			title_form.setStyleSheet("font: 12pt")
			self.addRow(title_form)
		
		#Series
		if book_list[index].series:
			series_str = f"<i>{book_list[index].series}</i>"
			if book_list[index].volume_in_series:
				series_str = f"{series_str} #{book_list[index].volume_in_series}"
			series_form = QLabel(series_str)
			series_form.setStyleSheet('font: 10pt')
			self.addRow(series_form)
			
		#Author
		if len(book_list[index].author) > 1 or book_list[index].author[0]:
			self.addRow(QLabel(f"<b>Author:</b> {'; '.join(book_list[index].author)}", wordWrap=True))
		
		#Translator
		if book_list[index].translator:
			self.addRow(QLabel(f"<b>Translator:</b> {book_list[index].translator}"))
			
		#Page count and format
		if book_list[index].num_pages or book_list[index].book_format or int(get_int(book_list[index].number_of_volumes)) > 1: 
			page_and_format_line = QHBoxLayout()
			if book_list[index].num_pages:
				page_and_format_line.addWidget(QLabel(f"<b>Length:</b> {book_list[index].num_pages} pages"))
			if book_list[index].book_format or int(get_int(book_list[index].number_of_volumes)) > 1:
				format_str = "<b>Format:</b>"
				if book_list[index].book_format:
					format_str = f"{format_str} {book_list[index].book_format}"
					if int(get_int(book_list[index].number_of_volumes)) > 1:
						format_str = f"{format_str}, {book_list[index].number_of_volumes} volumes"
				elif not book_list[index].book_format and int(get_int(book_list[index].number_of_volumes)) > 1:
					format_str = f"{format_str} {book_list[index].number_of_volumes} volumes"
				page_and_format_line.addWidget(QLabel(format_str))
			self.addRow(page_and_format_line)
			
		#Publisher and year publisher
		if book_list[index].publisher or book_list[index].edition_publication_year:
			publisher_line = QHBoxLayout()
			if book_list[index].publisher:
				publisher_line.addWidget(QLabel(f"<b>Published by:</b> {book_list[index].publisher}"))
			if book_list[index].edition_publication_year:
				publisher_line.addWidget(QLabel(f"<b>Publication year:</b> {book_list[index].edition_publication_year}"))
			self.addRow(publisher_line)

		#ISBN
		if book_list[index].isbn10 or book_list[index].isbn13:
			isbn_line = QHBoxLayout()
			if book_list[index].isbn10:
				isbn_line.addWidget(QLabel(f"<b>ISBN-10</b>: {book_list[index].isbn10}"))
			if book_list[index].isbn13:
				isbn_line.addWidget(QLabel(f"<b>ISBN-13</b>: {book_list[index].isbn13}"))
			self.addRow(isbn_line)
			
		#Collection
		if book_list[index].collection:
			collection_str = book_list[index].collection
			if book_list[index].volume_in_collection:
				collection_str = f"{collection_str} #{book_list[index].volume_in_collection}"
			self.addRow(QLabel(collection_str))
			
		#Original title
		if book_list[index].original_title:
			self.addRow(QLabel(f"<b>Original title:</b> {book_list[index].original_title}"))
			
		#Original publication year:
		if book_list[index].original_publication_year:
			self.addRow(QLabel(f"<b>Original publication year:</b> {book_list[index].original_publication_year}"))
			
		if book_list[index].weblink:
			weblink_form = QLabel(f'<b>Weblink:</b> <a href={book_list[index].weblink}>Open in browser</a>')
			weblink_form.setOpenExternalLinks(True)
			self.addRow(weblink_form)
			
		#Reading status header
		reading_status_header = QLabel("My reading status")
		reading_status_header.setStyleSheet('font: 11pt')
		self.addRow(reading_status_header)
		
		#Reading status and counter
		reading_line = QHBoxLayout()
		reading_line.addWidget(QLabel(f"<b>Reading status</b>: {book_list[index].reading_status}"))
		reading_line.addWidget(QLabel(f"<b>Read counter:</b> {book_list[index].times_read}"))
		self.addRow(reading_line)
		
		#Dates started and read
		if book_list[index].date_read or book_list[index].date_started:
			dates_line = QHBoxLayout()
			if book_list[index].date_read:
				dates_line.addWidget(QLabel(f"<b>Date read:</b> {book_list[index].date_to_ddmmmyyyy('date_read')}"))
			if book_list[index].date_started:
				dates_line.addWidget(QLabel(f"<b>Date started:</b> {book_list[index].date_to_ddmmmyyyy('date_started')}"))
			self.addRow(dates_line)
						
		#Rating and date added
		rating_line = QHBoxLayout()
		if book_list[index].rating:
			rating_line.addWidget(QLabel(f"<b>Rating:</b> {to_rating_cb(book_list[index].rating)}"))
		rating_line.addWidget(QLabel(f"<b>Date added:</b> {book_list[index].get_date_added_ddmmmyyyyhhmm()}"))
		self.addRow(rating_line)
			
		#bookshelves
		if len(book_list[index].bookshelves) > 1 or book_list[index].bookshelves[0]:
			self.addRow(QLabel(f"<b>Bookshelves:</b> {'; '.join(book_list[index].bookshelves)}", wordWrap=True))
				
		#Review
		if book_list[index].review:
			self.addRow(QLabel(f"<b>Review:</b> {book_list[index].review[0:64]}..."))
			
		edit_review_button = QPushButton()
		if book_list[index].review:
			edit_review_button.setText("Edit / Read Full Review")
		else:
			edit_review_button.setText("Add Review")
		edit_review_button.clicked.connect(lambda: main_window.get_quick_text_editor("review", index))
		self.addRow(edit_review_button)
		
		#Quotes
		edit_quotes_button = QPushButton()
		if book_list[index].quotes:
			edit_quotes_button.setText("Edit / Read All Quotes")
		else:
			edit_quotes_button.setText("Add Quotes")
		edit_quotes_button.clicked.connect(lambda: main_window.get_quick_text_editor("quotes", index))
		self.addRow(edit_quotes_button)
		
		#Notes
		edit_notes_button = QPushButton()
		if book_list[index].notes:
			edit_notes_button.setText("Edit / Read All Notes")
		else:
			edit_notes_button.setText("Add Notes")
		edit_notes_button.clicked.connect(lambda: main_window.get_quick_text_editor("notes", index))
		self.addRow(edit_notes_button)
		
		#User's copy header
		copy_header = QLabel("My copy")
		copy_header.setStyleSheet('font: 11pt')
		self.addRow(copy_header)
		if not book_list[index].bought_where \
				and not book_list[index].date_bought \
				and not book_list[index].condition:
			self.addRow(QLabel("(no details)"))

			
		if book_list[index].bought_where:
			self.addRow(QLabel(f"<b>Bought at:</b> {book_list[index].bought_where}"))
		if book_list[index].date_bought:
			self.addRow(QLabel(f"<b>Date bought:</b> {book_list[index].date_to_ddmmmyyyy('date_bought')}"))
		if book_list[index].condition:
			self.addRow(QLabel(f"<b>Condition:</b> {book_list[index].condition}"))

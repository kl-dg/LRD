from datetime import datetime

#Object lists
author_list = []
bookshelves_list = []
book_list = []
collection_list = []
publisher_list = []
series_list = []
year_list = []
year_read_list = []

#Indexes lists
search_list = []
books_by_author_list = []
books_by_series_or_collection = []
books_by_publisher = []
books_by_year_list = []
books_by_bookshelf_list = []
current_reading_list = []
to_read_list = []
wishlist = []
books_read_by_year_list = []
gave_up_list = []
research_books_list = []
not_read_list = []
text_box_list = []

class Book:
	"""
	Structured dictionary for every book in library.
	"""
	
	def __init__(
			self, 
			title="", 
			author="", 
			num_pages="", 
			publisher="", 
			rating="",
			date_read="", 
			isbn10="",
			isbn13="",
			date_added="",
			date_started="",
			reading_status="",
			book_format="",
			review="",
			edition_publication_year="",
			original_publication_year="",
			original_title="",
			series="",
			volume_in_series="",
			collection="",
			volume_in_collection="",
			times_read="",
			number_of_volumes="",
			translator="",
			weblink="",
			bought_where="",
			date_bought="",
			bookshelves="",
			condition="",
			quotes="",
			notes="",
			static_index=""
			):
					 
		self.title = title
		self.author = author
		self.num_pages = num_pages
		self.publisher = publisher
		self.rating = rating
		self.date_read = date_read
		self.isbn10 = isbn10
		self.isbn13 = isbn13
		self.reading_status = reading_status
		self.book_format = book_format
		self.date_added = date_added
		self.date_started = date_started
		self.review = review
		self.edition_publication_year = edition_publication_year
		self.original_publication_year = original_publication_year
		self.original_title = original_title
		self.series = series
		self.volume_in_series = volume_in_series
		self.collection = collection
		self.volume_in_collection = volume_in_collection
		self.times_read = times_read
		self.number_of_volumes = number_of_volumes
		self.translator = translator
		self.weblink = weblink
		self.bought_where = bought_where
		self.date_bought = date_bought
		self.bookshelves = bookshelves
		self.condition = condition
		self.quotes = quotes
		self.notes = notes
		self.static_index = static_index
		

	def author_sorted(self):
		"""
		Returns author's name, sortable by last name.
		"""
		
		if self.author[0] and ',' in self.author[0]: return self.author[0]
		elif self.author[0]: return f"{self.author[0].split()[-1]}, {' '.join(self.author[0].split()[0:-1])}"
		else: return ""
		
		
	def date_sortable(self, date_type):
		"""
		Returns requested date, if date is blank, replace by a dummy.
		"""
		
		if getattr(self, date_type): return getattr(self, date_type)
		else: return datetime.strptime('0001/01/01', '%Y/%m/%d')
		
		
	def get_date_as_string(self, date_type, formatting):
		"""
		Returns requested date as a string.
		"""
		
		if getattr(self, date_type):
			return getattr(self, date_type).strftime(formatting)

		
	def date_to_ddmmmyyyy(self, date_type):
		"""
		Returns requested date as a string dd/mmm/yyyy.
		"""
		
		if getattr(self, date_type): return getattr(self, date_type).strftime('%d/%b/%Y')

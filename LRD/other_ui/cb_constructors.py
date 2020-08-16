from PyQt5.QtWidgets import QComboBox

from functions.date_formatting import get_now_year
from library.strings import months

class DayDropDown(QComboBox):
	"""
	Creates a ComboBox with all the days of month, 1 to 31, preceded by
	an empty string to allow no date option.
	"""
	
	def __init__(self):
		super().__init__()
		self.addItem("")
		for day in range(1, 32):
			self.addItem(str(day))
			
			
class MonthDropDown(QComboBox):
	"""
	Creates a ComboBox with all months of the year, preceded by an empty
	string to allow no date option.
	"""
	
	def __init__(self):
		super().__init__()
		self.addItem("")
		for month in months:
			self.addItem(month)


class YearDropDown(QComboBox):
	"""
	Creates a ComboBox with all year from today till a century ago, 
	preceded by an empty string to allow no date option.
	"""
	
	def __init__(self):
		super().__init__()
		self.addItem("")
		year_counter = int(get_now_year())
		for year in range(0, 100):
			self.addItem(str(year_counter))
			year_counter -= 1


class FormatDropDown(QComboBox):
	"""
	ComboBox for book binding selection, ordered the way they should be 
	displayed.
	"""
	
	def __init__(self):
		super().__init__()
		self.addItem("Unspecified")
		self.addItem("Paperback")
		self.addItem("Pocketbook")
		self.addItem("Hardcover")
		self.addItem("Leatherbound")
		self.addItem("Library Binding")
		self.addItem("Spiral")
		self.addItem("Custom binding")
		self.addItem("Unbound")
		self.insertSeparator(10)
		self.addItem("Ebook")
		self.addItem("Kindle Ebook")
		self.addItem("Nook Ebook")
		self.insertSeparator(13)
		self.addItem("Audiobook")
		self.addItem("CD Audiobook")
		self.addItem("Cassete Audiobook")
		self.insertSeparator(17)
		self.addItem("Unknown")


class ReadingStatusDropDown(QComboBox):
	"""
	ComboBox for Reading Status selection.
	"""
	
	def __init__(self):
		super().__init__()
		self.addItem("Not read")
		self.addItem("Wishlist")
		self.addItem("To read")
		self.addItem("Currently reading")
		self.addItem("Read")
		self.addItem("Gave up")
		self.addItem("For research")


class RatingDropDown(QComboBox):
	"""
	ComboBox for rating selection, including "Not rated" option.
	"""
	
	def __init__(self):
		super().__init__()
		self.addItem("Not rated")
		self.addItem("1 star")
		self.addItem("2 stars")
		self.addItem("3 stars")
		self.addItem("4 stars")
		self.addItem("5 stars")
		
		
class FieldDropDown(QComboBox):
	"""
	ComboBox for attribute selection in search tab.
	"""
	
	def __init__(self):
		super().__init__()
		self.addItem("Title")
		self.addItem("Author")
		self.addItem("Series")
		self.addItem("Publisher")
		self.addItem("Bookshelves")
		self.addItem("Review")
		self.addItem("Quotes")
		self.addItem("Notes")


class SortReviewsDropDown(QComboBox):
	"""
	ComboBox for sorting reviews, quotes or notes.
	"""
	
	def __init__(self):
		super().__init__()
		self.addItem("Title")
		self.addItem("Author")
		self.addItem("Rating")
		self.addItem("Date Read")
		self.addItem("Book Length")
		self.addItem("Publication Year")
		

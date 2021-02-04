from PyQt5.QtWidgets import QWidget

from functions.value_calculations import average
from library.book_library import library

class GenericMainWindowTab(QWidget):
	"""
	Attributes common to all main window tabs.
	"""
	
	def __init__(self, main_window):
		super().__init__()
		self.main_window = main_window
		self.is_outdated = True
		
		
	def get_list_by_attribute(self, working_list, attribute, get_avg_length = False):
		"""
		Fills a list with stats by attribute value.
		
		args:		
		working_list: output list, such as <author_list>.
		
		attribute: what book attribute, such as 'author'.
		
		get_avg_length: either True of False, depending if this information
		is relevant for the table.
		"""
		
		working_list.clear()
		attribute_set = set()
		for book in library.values():
			if getattr(book, attribute):
				attribute_set.add(getattr(book, attribute))
				
		attribute_dict = dict()
		for attribute_ in attribute_set:
			attribute_dict[attribute_] = [0, 0, 0, 0, 0]
			
		for book in library.values():
			try:
				attribute_dict[getattr(book, attribute)][0] += 1
				if book.rating:
					attribute_dict[getattr(book, attribute)][1] += 1
					attribute_dict[getattr(book, attribute)][2] += int(book.rating)
				if book.num_pages and get_avg_length:
					attribute_dict[getattr(book, attribute)][3] += 1
					attribute_dict[getattr(book, attribute)][4] += int(book.num_pages)
			except KeyError: pass
		
		if get_avg_length:
			for key, value in attribute_dict.items():
				working_list.append(dict(
					title = key, 
					book_count = value[0],
					average_rating = f"{average(value[2], value[1]):.2f}",
					average_length = f"{average(value[4], value[3]):.2f}",
					))
	
		else:
			for key, value in attribute_dict.items():
				working_list.append(dict(
					title = key,
					book_count = value[0],
					average_rating = f"{average(value[2], value[1]):.2f}",
					))

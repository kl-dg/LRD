from library.book_library import library, books_by_publisher

def get_books_by_publisher(selected_publisher):
	"""
	Refreshes list of books by selected publisher
	"""
	
	books_by_publisher.clear()
	[books_by_publisher.append(index) for index in library if library[index].publisher == selected_publisher]

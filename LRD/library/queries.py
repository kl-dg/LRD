from functions.value_calculations import average
from library.book_library import library, books_by_bookshelf_list, books_by_publisher, bookshelves_list


def get_bookshelves_list():
	"""
	Refreshes list of bookshelves. 
	
	Finds every unique bookshelf in library and add to bookshelves list a dictionary containing
	the bookshelf name, book count, average rating and page count.
	"""
	
	#Clear current list of bookshelves
	bookshelves_list.clear()
	
	#Make a set with all unique bookshelves' names
	bookshelves_set = set()
	for book in library.values():
		if len(book.bookshelves) > 1 or book.bookshelves[0]:
			for shelf in book.bookshelves:
				bookshelves_set.add(shelf)
	
	#Make a dictionary to hold information about each bookshelf
	bookshelves_dict = dict()
	for shelf in bookshelves_set:
		bookshelves_dict[shelf] = [0, 0, 0, 0, 0]
		
	#Loop through the library in order to get book count, average rating and page count for each bookshelf
	for book in library.values():
		if len(book.bookshelves) > 1 or book.bookshelves[0]:
			for shelf in book.bookshelves:
				bookshelves_dict[shelf][0] += 1
				if book.rating:
					bookshelves_dict[shelf][1] += int(book.rating)
					bookshelves_dict[shelf][2] += 1
				if book.num_pages:
					bookshelves_dict[shelf][3] += int(book.num_pages)
					bookshelves_dict[shelf][4] += 1
					
	#Add bookshelf dictionary to bookshelves list
	for key, value in bookshelves_dict.items():
		bookshelves_list.append(dict(
			bookshelf = key,
			book_count = value[0],
			average_rating = f"{average(value[1], value[2]):.2f}",
			average_length = f"{average(value[3], value[4]):.2f}",
			))
			

def get_books_by_bookshelf(selected_bookshelf):
	"""
	Refreshes list of books by selected bookshelf
	"""
	
	books_by_bookshelf_list.clear()
	[books_by_bookshelf_list.append(index) for index in library if selected_bookshelf in library[index].bookshelves]
				
				
def get_books_by_publisher(selected_publisher):
	"""
	Refreshes list of books by selected publisher
	"""
	
	books_by_publisher.clear()
	[books_by_publisher.append(index) for index in library if library[index].publisher == selected_publisher]

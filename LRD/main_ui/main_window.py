from PyQt5.QtWidgets import (
	QDialog,
	QFileDialog,
	QMainWindow,
	QMessageBox,
	QTabWidget,
	QVBoxLayout,
	QWidget,
	)
	
from main_ui.toolbar import ToolBar

from library.book_library import library
from library.edit_library import delete_book
	
from library.file_io import (
	write_to_file,
	load_file,
	import_from_file,
	)

from dialogs.close_program import AskSaveBeforeQuit
from dialogs.edit_attribute import EditValueByAttribute
from dialogs.edit_book import EditBook
from dialogs.delete_book import DeleteBook
from dialogs.import_assistant import ImportAssistant 
from dialogs.new_file import ConfirmNewLibrary
from dialogs.quick_text_editor import EditText
from mw_tabs.tab_library import LibraryTab
from mw_tabs.tab_search import SearchTab
from mw_tabs.tab_author import AuthorTab
from mw_tabs.tab_series import SeriesTab
from mw_tabs.tab_publisher import PublisherTab
from mw_tabs.tab_publishing_year import PublishingYearTab
from mw_tabs.tab_bookshelves import BookshelvesTab
from mw_tabs.tab_reading import ReadingTab
from mw_tabs.tab_reviews import TextPageTab
					 				 		 

class MainWindow(QMainWindow):
	"""
	Program's main window layout and methods for calling dialogs.
	"""
	
	def __init__(self):
		super().__init__()
		self.working_file = ""
		self.flag_unsaved_changes = False
		
		self.setWindowTitle("Library Rat's Diary")
		self.resize(1280, 720)
		
		#Toolbar
		toolbar = ToolBar(self)
		self.addToolBar(toolbar)
		
		#Declaring and adding tabs
		self.tab_library = LibraryTab(self)
		self.tab_search = SearchTab(self)
		self.tab_author = AuthorTab(self)
		self.tab_series = SeriesTab(self)
		self.tab_publisher = PublisherTab(self)
		self.tab_publication_year = PublishingYearTab(self)
		self.tab_reading_progress = ReadingTab(self)
		self.tab_bookshelves = BookshelvesTab(self)
		self.tab_reviews = TextPageTab(self, 'review')
		self.tab_quotes = TextPageTab(self, 'quotes')
		self.tab_notes = TextPageTab(self, 'notes')
		
		self.main_window_tabs = QTabWidget()
		self.main_window_tabs.addTab(self.tab_library, "Library")
		self.main_window_tabs.addTab(self.tab_search, "Search")
		self.main_window_tabs.addTab(self.tab_author, "Author")
		self.main_window_tabs.addTab(self.tab_series, "Series")
		self.main_window_tabs.addTab(self.tab_publisher, "Publisher")
		self.main_window_tabs.addTab(self.tab_publication_year, "Publication Year")
		self.main_window_tabs.addTab(self.tab_reading_progress, "Reading Progress")
		self.main_window_tabs.addTab(self.tab_bookshelves, "Bookshelves")
		self.main_window_tabs.addTab(self.tab_reviews, "Reviews")
		self.main_window_tabs.addTab(self.tab_quotes, "Quotes")
		self.main_window_tabs.addTab(self.tab_notes, "Notes")
		self.main_window_tabs.currentChanged.connect(self.tab_click)
		
		main_layout = QVBoxLayout()
		main_layout.addWidget(self.main_window_tabs)
		
		self.central_widget = QWidget()
		self.central_widget.setLayout(main_layout)
		self.setCentralWidget(self.central_widget)
				
		
	def tab_click(self, index):
		"""
		Gets what tab was clicked and calls method to refresh their
		content.
		"""
		
		if index == 0: self.tab_library.refresh_tab()
		elif index == 1: self.tab_search.refresh_tab()
		elif index == 2: self.tab_author.refresh_tab()
		elif index == 3: self.tab_series.refresh_tab()
		elif index == 4: self.tab_publisher.refresh_tab()
		elif index == 5: self.tab_publication_year.refresh_tab()
		elif index == 6: self.tab_reading_progress.refresh_tab()
		elif index == 7: self.tab_bookshelves.refresh_tab()
		elif index == 8: self.tab_reviews.refresh_interface()
		elif index == 9: self.tab_quotes.refresh_interface()
		elif index == 10: self.tab_notes.refresh_interface()
		
		
	def refresh_current_tab(self):
		"""
		Whenever something is changed, refresh UI.
		"""
		
		if self.main_window_tabs.currentIndex() == 0: self.tab_library.refresh_tab()
		elif self.main_window_tabs.currentIndex() == 1: self.tab_search.refresh_tab()
		elif self.main_window_tabs.currentIndex() == 2: self.tab_author.refresh_tab()
		elif self.main_window_tabs.currentIndex() == 3: self.tab_series.refresh_tab()
		elif self.main_window_tabs.currentIndex() == 4: self.tab_publisher.refresh_tab()
		elif self.main_window_tabs.currentIndex() == 5: self.tab_publication_year.refresh_tab()
		elif self.main_window_tabs.currentIndex() == 6: self.tab_reading_progress.refresh_tab()
		elif self.main_window_tabs.currentIndex() == 7: self.tab_bookshelves.refresh_tab()
		elif self.main_window_tabs.currentIndex() == 8: self.tab_reviews.refresh_interface()
		elif self.main_window_tabs.currentIndex() == 9: self.tab_quotes.refresh_interface()
		elif self.main_window_tabs.currentIndex() == 10: self.tab_notes.refresh_interface()
			

	def new_file(self):
		"""
		Checks if there are unsaved changes then resets library, its 
		index list, working file and tab selections.
		"""
		
		if self.flag_unsaved_changes == True:
			self.confirm_new_library = ConfirmNewLibrary(self, 'new')
			self.confirm_new_library.exec_()
		else:
			library.clear()
			self.working_file = ""
			self.reset_tab_selections()
			self.set_interface_outdated()
			self.refresh_current_tab()
	
	
	def check_before_open_file(self):
		"""
		Checks if there are unsaved changes before opening a new 
		library file. Prompt user to save, discard or cancel if there
		are.
		"""
		
		if self.flag_unsaved_changes == True:
			self.ask_open_file = ConfirmNewLibrary(self, 'open')
			self.ask_open_file.exec_()
		else:
			self.open_file()
	
			
	def open_file(self):
		"""
		Asks user for a file to open, if received one, erase currently
		loaded library, its index list, reset and refresh tabs, then
		load the new library.
		"""

		try:
			file_path = QFileDialog.getOpenFileName(self,
				"Open file:", 
				"",
				"CSV Files (*.csv)")
			if file_path[0]:
				library.clear()
	
				load_file(file_path[0])
				self.set_interface_outdated()
				self.reset_tab_selections()
				self.refresh_current_tab()
				self.working_file = file_path[0]
				self.flag_unsaved_changes = False
				
				
		except PermissionError: self.permission_error_msgbox()
		except (ValueError, IndexError): self.value_error_msgbox()
		
		
	def open_import_assistant(self):
		"""
		Opens import assistant dialog with importing options.
		"""
		
		self.import_assistant = ImportAssistant(self)
		self.import_assistant.show()
						
					
	def import_from_gr(self, last_name_first, get_additional_authors):
		"""
		Imports from Goodreads library export CSV file and appends to
		book list.
		"""
		
		try:
			file_path = QFileDialog.getOpenFileName(self,
				"Open Goodreads library export file:", 
				"",
				"CSV Files (*.csv)")
			if file_path[0]:
				import_from_file(file_path[0], last_name_first, get_additional_authors)
				self.flag_unsaved_changes = True
				self.set_interface_outdated()
				self.refresh_current_tab()
				
				
		except PermissionError: self.permission_error_msgbox()
		except (ValueError, IndexError): self.value_error_msgbox()
		
		
	def merge_libraries(self):
		"""
		Opens a library previously create with this application and
		appends to the currently open library.
		"""
		
		try:
			file_path = QFileDialog.getOpenFileName(self,
				"Open file:",
				"",
				"CSV Files (*.csv)")
				
			if file_path[0]:
				load_file(file_path[0])
				self.flag_unsaved_changes = True
				self.set_interface_outdated()
				self.refresh_current_tab()
			
		except PermissionError: self.permission_error_msgbox()
		except (ValueError, IndexError): self.value_error_msgbox()
	
	
	def save_file(self):
		"""
		Saves to current open file, if no <self.working_file>, calls
		<self.save_as>.
		"""
		
		try:
			if self.working_file:
				write_to_file(self.working_file)
				self.flag_unsaved_changes = False
			else:
				self.save_as()
				
		except PermissionError:
			self.permission_error_msgbox()
	
	
	def save_as(self):
		"""
		Propts user to place where to write file, if a file_path was 
		received, write library to .csv file.
		"""
		
		try:
			file_path = QFileDialog.getSaveFileName(self,
				"Save file:", 
				"",
				"CSV Files (*.csv)")
	
			if file_path[0]:
				write_to_file(file_path[0])
				self.working_file = file_path[0]
				self.flag_unsaved_changes = False
		
		except PermissionError: 
			self.permission_error_msgbox()
		
			
	def add_book(self):
		"""
		Calls an empty EditBook dialog so user can add a new book, then
		refresh UI.
		"""
		
		self.add_book_ = EditBook(self)
		self.add_book_.show()
		
		
	def edit_book(self):
		"""
		Calls EditBook dialog for editing selected book, if there's a
		selected book. Then refresh UI.
		"""
		
		index = self.get_selected_book()
		if index is not None:
			self.edit_book_ = EditBook(self, index)
			self.edit_book_.show()
			
			
	def get_quick_text_editor(self, mode, index):
		"""
		Opens a quick text editor for editing reviews, quotes or notes.
		
		args:
		mode: selected attribute. Either 'review', 'quotes' or 'notes'.
		
		index: selected book's static library index.
		"""
		   
		if index is not None:
			self.quick_text_editor = EditText(index, mode, self)
			self.quick_text_editor.exec_()
			
			
	def edit_attribute(self, value, attribute):
		"""
		Opens a dialog for batch editing all books that share the same
		value on an attribute.
		
		args:
		value: attribute value, such as author's name.
		
		attribute: selected attribute, such as 'author', 'publisher', 
		'series'.
		"""
		
		self.edit_attribute_ = EditValueByAttribute(value, attribute, self)
		self.edit_attribute_.exec_()
		self.refresh_current_tab()
			
			
	def prompt_delete_book(self, index):
		"""
		Prompts user for confirmation on book deletion and returns
		answer.
		
		args:
		index: book's static library index.
		"""
		
		delete_book_ = DeleteBook(index)
		answer = delete_book_.exec_()
		return answer == QDialog.Accepted

					
	def clicked_delete_book(self):
		"""
		Gets selected book, if there's a selected book and user
		confirmed deletion, remove book and refresh UI.
		"""
		   
		index = self.get_selected_book()
		if index is not None:
			if self.prompt_delete_book(index):
				delete_book(index)
				self.flag_unsaved_changes = True
				self.set_interface_outdated()
				self.refresh_current_tab()
				
				
	def set_interface_outdated(self):
		"""
		Whenever a change is made, set all tabs to outdated.
		"""
		
		self.tab_library.is_outdated = True
		self.tab_search.is_outdated = True
		self.tab_author.is_outdated = True
		self.tab_series.is_outdated = True
		self.tab_publisher.is_outdated = True
		self.tab_publication_year.is_outdated = True
		self.tab_reading_progress.is_outdated = True
		self.tab_bookshelves.is_outdated = True
		self.tab_reviews.is_outdated = True
		self.tab_quotes.is_outdated = True
		self.tab_notes.is_outdated = True
		
		
	def reset_tab_selections(self):
		"""
		Reset UI when user starts a new library or open another library
		from file, such as selected author whose books would be shown
		in books by author table.
		"""
		
		self.tab_author.reset_selections()
		self.tab_bookshelves.reset_selections()
		self.tab_library.reset_selections()
		self.tab_publication_year.reset_selections()
		self.tab_publisher.reset_selections()
		self.tab_reading_progress.reset_selections()
		self.tab_search.reset_selections()
		self.tab_series.reset_selections()
		
				
	def get_selected_book(self):
		"""
		Checks what tab is open and if there's a selected book.
		Return book's library index.
		"""
		
		if self.main_window_tabs.currentIndex() == 0:
			if self.tab_library.selected_book is not None: return self.tab_library.selected_book
			
		elif self.main_window_tabs.currentIndex() == 1:
			if self.tab_search.selected_book is not None: return self.tab_search.selected_book
			
		elif self.main_window_tabs.currentIndex() == 2:
			if self.tab_author.selected_book is not None: return self.tab_author.selected_book
			
		elif self.main_window_tabs.currentIndex() == 3:
			if self.tab_series.selected_book is not None: return self.tab_series.selected_book
				
		elif self.main_window_tabs.currentIndex() == 4:
			if self.tab_publisher.selected_book is not None: return self.tab_publisher.selected_book
				
		elif self.main_window_tabs.currentIndex() == 5:
			if self.tab_publication_year.selected_book is not None: return self.tab_publication_year.selected_book
				
		elif self.main_window_tabs.currentIndex() == 6:
			if self.tab_reading_progress.selected_book is not None: return self.tab_reading_progress.selected_book
				
		elif self.main_window_tabs.currentIndex() == 7:
			if self.tab_bookshelves.selected_book is not None: return self.tab_bookshelves.selected_book
		
		
	def permission_error_msgbox(self):
		"""
		Message box for PermissionError exception on opening or 
		saving file.
		"""
		
		QMessageBox.warning(self, "File Error", 
				"You don't have permission to access or edit this file or it is being used by other application.", 
				QMessageBox.Ok)
				
				
	def value_error_msgbox(self):
		"""
		Message box for ValueError exception on opening or importing 
		file.
		"""
		
		QMessageBox.warning(self, "File Error", 
				"Couldn't read file: wrong file formatting.", 
				QMessageBox.Ok)
				
				
	def closeEvent(self, event):
		"""
		Checks for unsaved changes when user tries to close program. If 
		there are unsaved changes, prompt user to save, discard or 
		cancel. If user choose to save file, call this function
		recursively to check if the saving process was successful, user
		will prompted again if it wasn't.
		"""
		
		if self.flag_unsaved_changes:
			self.answer_close = 'ignore'
			self.get_answer = AskSaveBeforeQuit(self)
			self.get_answer.exec_()
			if self.answer_close == 'ignore': event.ignore()
			elif self.answer_close == 'accept': event.accept()
			elif self.answer_close == 'save':
				self.save_as()
				event.ignore()
				self.closeEvent(event)
			
		else: event.accept()

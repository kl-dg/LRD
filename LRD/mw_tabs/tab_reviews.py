from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
	QHBoxLayout, 
	QLabel,
	QPushButton,
	QSizePolicy,
	QScrollArea, 
	QTextEdit,  
	QVBoxLayout,
	QWidget, 
	)

from functions.string_formatting import get_int
from library.book_library import reviews_list, quotes_list, notes_list, library
from library.queries import get_books_with_text
from mw_tabs.main_window_tab import GenericMainWindowTab
from other_ui.cb_constructors import SortReviewsDropDown


class TextPageTab(GenericMainWindowTab):
	"""
	Reusable layout for Reviews, Quaotes and Notes tabs on main window.
	
	Tab Layout:
	Central blog-like scrollable area with book's title, selected
	information and a text box containing either reviews, quotes or
	notes.
	
	self.text_page_layout: covers the entire screen width.
		
	self.text_boxes_area: central area, where the blog-like layout
	will be.
	
	self.text_boxes_area_layout: <self.text_boxes_area> layout.
	
	args:
	main_window: parent reference for using its methods.
	
	attribute: tab content. Either 'review', 'quotes' or 'notes'.
	"""
	
	def __init__(self, main_window, attribute):
		super().__init__(main_window)
		self.attribute = attribute
		
		#This constructor can handle review, quotes and notes tabs. There's a specific list for each of these
		#attributes, the following two lines will correlate self.text_box_list to the proper list.
		self.attribute_lists = {"review": reviews_list, "quotes": quotes_list, "notes": notes_list}
		self.text_box_list = self.attribute_lists[self.attribute]
		
		self.sort_cb = SortReviewsDropDown()
		self.sort_cb.currentTextChanged.connect(lambda: self.refresh_interface(sorting=True))
		
		widgets_bar = QHBoxLayout()
		widgets_bar.addWidget(QLabel("Sort by:"))
		widgets_bar.addWidget(self.sort_cb)
		widgets_bar.addStretch()
		
		self.text_boxes_area_layout = QVBoxLayout()
		self.text_boxes_area_layout.addLayout(widgets_bar)
		
		text_boxes_area = QWidget()
		text_boxes_area.setLayout(self.text_boxes_area_layout)
		text_boxes_area.setFixedWidth(700)
		
		text_page_layout = QHBoxLayout(self)
		text_page_layout.addWidget(text_boxes_area, Qt.AlignCenter)

		self.text_boxes_area_settings()
		
	
	def text_boxes_area_settings(self):
		"""		
		self.v_scroll: is added to <self.text_boxes_area_layout> to 
		allow scrollable content inside of it.
		
		self.scrollable_content: is added to <self.v_scroll> in order
		to be scrollable.
		
		self.scrollable_content_layout: <self.scrollable_content> 
		layout, where books' reviews, quotes or notes will be added to.
		"""
		
		self.scrollable_content_layout = QVBoxLayout()
		self.scrollable_content_layout.addStretch()
		
		self.scrollable_content = QWidget()
		self.scrollable_content.setLayout(self.scrollable_content_layout)
		
		self.v_scroll = QScrollArea()
		self.v_scroll.setWidgetResizable(True)
		self.v_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.v_scroll.setWidget(self.scrollable_content)
		
		self.text_boxes_area_layout.addWidget(self.v_scroll)

	
	def refresh_interface(self, sorting=False):
		"""
		Refreshes central blog-like widget. First delete it, if yet
		not deleted. Then redeclare it, get a list of books with a 
		review, quotes or notes and add them to the interface.
		"""
		
		if self.is_outdated or sorting:
			self.text_boxes_area_layout.removeWidget(self.v_scroll)
			self.v_scroll.deleteLater()
			
			self.text_boxes_area_settings()
			if not sorting:
				get_books_with_text(self.attribute, self.attribute_lists[self.attribute])
			self.sort_tab()
			for index in self.text_box_list:
				book_widget = BookWidget(self, index, self.attribute)
				self.scrollable_content_layout.addWidget(book_widget)
			self.is_outdated = False
			
	
	def edit_text_box(self, attribute, index):
		"""
		Calls quick text editor when user clicks on 'Edit' button.
		
		args:
		attribute: 'review', 'quotes' or 'notes'.
		
		index: book's static library index.
		"""
		
		self.main_window.get_quick_text_editor(attribute, index)
		self.refresh_interface()
		
	
	def sort_tab(self):
		"""
		Sort books according to user selection.
		"""
		
		if self.sort_cb.currentIndex() == 0: 
			self.text_box_list.sort(key = lambda x: library[x].title.lower())
		elif self.sort_cb.currentIndex() == 1:
			self.text_box_list.sort(key = lambda x: library[x].author_sorted().lower())
		elif self.sort_cb.currentIndex() == 2:
			self.text_box_list.sort(key = lambda x: library[x].rating, reverse=True)
		elif self.sort_cb.currentIndex() == 3:
			self.text_box_list.sort(key = lambda x: library[x].date_sortable('date_read'), reverse=True)
		elif self.sort_cb.currentIndex() == 4:
			self.text_box_list.sort(key = lambda x: get_int(library[x].num_pages), reverse=True)
		elif self.sort_cb.currentIndex() == 5:
			self.text_box_list.sort(key = lambda x: get_int(library[x].original_publication_year), reverse=True)
			
	
class BookWidget(QWidget):
	"""
	Layout for a blog-like post representing a book review, or its 
	quotes or notes.
	
	args:
	parent: reference to main window, to allow the use of its methods.
	
	index: book's static library index.
	
	attribute: either 'review', 'quotes' or 'notes'.
	"""
	
	def __init__(self, parent, index, attribute):
		super().__init__()
		book = library[index]
		
		if book.title: title = QLabel(book.title)
		else: title = QLabel("(No Title)")
		title.setWordWrap(True)
		title.setStyleSheet('font: 14pt')
		
		information_line_layout = QHBoxLayout()
		
		if len(book.author) > 0:
			information_line_layout.addWidget(QLabel(f"by {'; '.join(book.author)}", wordWrap=True), 10)
		else:
			information_line_layout.addWidget(QLabel("(no author)"), 10)
			
		if book.date_read:
			information_line_layout.addWidget(QLabel(f"<b>Date read:</b> {book.get_date_as_string('date_read', '%d/%b/%Y')}"), 2)
		if book.rating:
			information_line_layout.addWidget(QLabel(f"<b>Rating:</b> {book.rating}"), 2)
		
		button_edit = QPushButton()
		button_edit.setText("Edit")
		button_edit.clicked.connect(lambda: parent.edit_text_box(attribute, index))
		information_line_layout.addWidget(button_edit, 1)
			
		text_box = TextBox(getattr(book, attribute))
		
		book_widget_layout = QVBoxLayout(self)
		book_widget_layout.addWidget(title)
		book_widget_layout.addLayout(information_line_layout)
		book_widget_layout.addWidget(text_box)
		
		
		
class TextBox(QTextEdit):
	"""
	Modifies QTextEdit to disable scrollbars, set read-only and fit
	height to contents.
	
	args:
	text: text content of review, quotes or notes.
	"""
	
	def __init__(self, text):
		super().__init__()
		
		self.setText(text)
		self.setReadOnly(True)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.setFixedWidth(620)
		#Hide and redisplay for dynamic resizing to take effect.
		self.setAttribute(Qt.WA_DontShowOnScreen)
		self.show()
		self.setFixedHeight(self.document().size().height() + self.contentsMargins().top() + self.contentsMargins().bottom())

		

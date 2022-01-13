from PyQt5.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from data.index_lists import search_results
from control.queries import search_in_library
from ui.misc.cb_constructors import FieldDropDown
from ui.info_panel.refresh import refresh_panel
from ui.info_panel.empty_panel import EmptyPanel
from ui.tables.book_table import BookTable



class SearchTab(QWidget):
	"""
	Layout for Search Tab in main window.
	
	Tab Layout: 
	self.layout: divides screen horizontally, Info Panel on
	right side, search fields and result table on left side.
	
	self.search_panel: splits vertically the left side of the screen.
	Top line contains search fields, bottom contains search results
	<self.search_table>.
	
	args:	
	attributes:
	self.current_search_input: value in search field last time Search 
	button was pressed.
	
	self.current_search_field: attribute to be searched last time Search 
	button was pressed.
	
	self.current_search_case_sensitive: case sensitive boolean last time 
	Search button was pressed. Default: False.
	
	self.selected_book: last book clicked, for displaying in Info Panel.
	"""
	
	def __init__(self):
		super().__init__()
		self.is_outdated = True
		self.current_search_input = ""
		self.current_search_field = ""
		self.current_search_case_sensitive = False
		self.selected_book = None
		
		self.search_prompt_settings()
		self.search_table = BookTable(self, search_results)
		
		search_panel = QVBoxLayout()
		search_panel.addWidget(self.search_prompt)
		search_panel.addWidget(self.search_table)
		
		self.panel = EmptyPanel()
		
		self.layout = QHBoxLayout(self)
		self.layout.addLayout(search_panel)
		self.layout.addWidget(self.panel)

		
	def search_prompt_settings(self):
		"""
		Layout for search field and searching options.
		"""

		self.search_input_field = QLineEdit()
		self.search_input_field.resize(15, 200)
		self.search_input_field.returnPressed.connect(lambda: search_button.click())
		
		self.search_in_cb = FieldDropDown()
		
		self.case_sensitive_check = QCheckBox()
		self.case_sensitive_check.setText("Case sensitive")
		
		search_button = QPushButton()
		search_button.setText("Search")
		search_button.clicked.connect(self.search_perform)
		
		search_prompt_layout = QHBoxLayout()
		search_prompt_layout.addWidget(QLabel("Search:"))
		search_prompt_layout.addWidget(self.search_input_field)
		search_prompt_layout.addWidget(QLabel("in"))
		search_prompt_layout.addWidget(self.search_in_cb)
		search_prompt_layout.addWidget(self.case_sensitive_check)
		search_prompt_layout.addWidget(search_button)
		
		self.search_prompt = QWidget()
		self.search_prompt.setLayout(search_prompt_layout)
		self.search_prompt.setMaximumWidth(500)
		
		
	def search_perform(self):
		"""
		Writes down search input and options then calls function that
		retrieves matching results.
		"""
		
		if len(self.search_input_field.text()) > 0:
			self.current_search_input = self.search_input_field.text()
			self.current_search_field = self.search_in_cb.currentText()
			self.current_search_case_sensitive = self.case_sensitive_check.isChecked()
			
			self.refresh_search_results()
							
		
	def refresh_tab(self):
		"""
		When user comes back to search tab, refresh search results and
		Info Panel.
		"""
		
		if self.is_outdated:
			self.refresh_search_results()
			refresh_panel(self)
			self.is_outdated = False
		
		
	def reset_selections(self):
		"""
		When user opens other library, reset search results, search
		input and Info Panel.
		"""
		
		search_results.clear()
		self.current_search_input = ""
		self.search_input_field.setText("")
		self.selected_book = None
		
		
	def refresh_search_results(self):
		"""
		Do a search and refresh search results.
		"""
		
		if len(self.current_search_input) > 0:
			search_in_library(self.current_search_input, self.current_search_field, self.current_search_case_sensitive)
								
		self.search_table.refresh_table()

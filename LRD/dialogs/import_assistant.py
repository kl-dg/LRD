from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
	QButtonGroup,
	QCheckBox,
	QHBoxLayout,
	QLabel,
	QPushButton,
	QRadioButton,
	QVBoxLayout,
	QWidget,
	)


class ImportAssistant(QWidget):
	"""
	Assistant for importing libraries.
	
	args:
	main_window: reference to parent widget in order to use its methods.
	"""
	
	def __init__(self, main_window):
		super().__init__()
		self.main_window = main_window
		self.setWindowIcon(QIcon('icons/import.png'))
		self.setWindowTitle("Import Library")
		self.setWindowModality(Qt.ApplicationModal)
		self.setWindowFlags(Qt.WindowCloseButtonHint)
		self.resize(500, 300)
		
		self.import_selection = 'gr'
		self.gr_naming_selection = False
		self.gr_additional_authors_selection = True
		
		self.cancel_button = QPushButton("Cancel")
		self.cancel_button.clicked.connect(self.close)
		
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)
		self.load_selection_screen()
		
		
	def load_selection_screen(self):
		"""
		First screen of importing assistant. Let user choose between
		importing sources.
		"""
		
		option_gr = QRadioButton("Import from Goodreads library")
		option_gr.clicked.connect(lambda: setattr(self, 'import_selection', 'gr'))
		if self.import_selection == 'gr': option_gr.setChecked(True)
		
		option_merge = QRadioButton("Merge libraries")
		option_merge.clicked.connect(lambda: setattr(self, 'import_selection', 'merge'))
		if self.import_selection == 'merge': option_merge.setChecked(True)
		
		import_type_selection = QButtonGroup(self)
		import_type_selection.addButton(option_gr)
		import_type_selection.addButton(option_merge)

		next_button = QPushButton("Next")
		next_button.clicked.connect(self.get_import_options_screen)
		
		sel_screen_buttons_layout = QHBoxLayout()
		sel_screen_buttons_layout.addStretch()
		sel_screen_buttons_layout.addWidget(self.cancel_button)
		sel_screen_buttons_layout.addWidget(next_button)
		
		import_selection_screen_layout = QVBoxLayout()
		import_selection_screen_layout.addWidget(QLabel("Select import source:"))
		import_selection_screen_layout.addWidget(option_gr)
		import_selection_screen_layout.addWidget(option_merge)
		import_selection_screen_layout.addStretch()
		import_selection_screen_layout.addLayout(sel_screen_buttons_layout)
		
		self.import_selection_screen = QWidget()
		self.import_selection_screen.setLayout(import_selection_screen_layout)
		self.layout.addWidget(self.import_selection_screen)
		
		
	def get_import_options_screen(self):
		"""
		Calls the 2nd screen depending on user's choice on the first.
		"""
		
		self.layout.removeWidget(self.import_selection_screen)
		self.import_selection_screen.deleteLater()
		
		if self.import_selection == 'gr': self.load_gr_import_options_screen()
		elif self.import_selection == 'merge': self.load_merge_import_options_screen()
		
	
	def load_gr_import_options_screen(self):
		"""
		Layout for importing options after user choose to import from
		GR library export file.
		"""
		
		gr_naming_format_first = QRadioButton('"First Last"')
		gr_naming_format_first.clicked.connect(lambda: setattr(self, 'gr_naming_selection', False))
		if self.gr_naming_selection == False: gr_naming_format_first.setChecked(True)
		
		gr_naming_format_last = QRadioButton('"Last, First"')
		gr_naming_format_last.clicked.connect(lambda: setattr(self, 'gr_naming_selection', True))
		if self.gr_naming_selection == True: gr_naming_format_last.setChecked(True)
		
		gr_naming_format_selection = QButtonGroup(self)
		gr_naming_format_selection.addButton(gr_naming_format_first)
		gr_naming_format_selection.addButton(gr_naming_format_last)
		
		gr_import_additional_authors_choice = QCheckBox("Import additional authors")
		gr_import_additional_authors_choice.stateChanged.connect(lambda: setattr(self, 'gr_additional_authors_selection', gr_import_additional_authors_choice.isChecked()))
		if self.gr_additional_authors_selection: gr_import_additional_authors_choice.setChecked(True)
		
		gr_back_button = QPushButton("Back")
		gr_back_button.clicked.connect(self.back_from_gr_options)
		
		gr_import_button = QPushButton("Import")
		gr_import_button.clicked.connect(self.gr_import)
		
		gr_options_buttons_layout = QHBoxLayout()
		gr_options_buttons_layout.addStretch()
		gr_options_buttons_layout.addWidget(self.cancel_button)
		gr_options_buttons_layout.addWidget(gr_back_button)
		gr_options_buttons_layout.addWidget(gr_import_button)
		
		gr_options_screen_layout = QVBoxLayout()
		gr_options_screen_layout.addWidget(QLabel("GoodReads importing options"))
		gr_options_screen_layout.addWidget(QLabel(""))
		gr_options_screen_layout.addWidget(QLabel("Author names format:"))
		gr_options_screen_layout.addWidget(gr_naming_format_first)
		gr_options_screen_layout.addWidget(gr_naming_format_last)
		gr_options_screen_layout.addWidget(QLabel(""))
		gr_options_screen_layout.addWidget(gr_import_additional_authors_choice)
		gr_options_screen_layout.addStretch()
		gr_options_screen_layout.addLayout(gr_options_buttons_layout)
		
		self.gr_options_screen = QWidget()
		self.gr_options_screen.setLayout(gr_options_screen_layout)
		self.layout.addWidget(self.gr_options_screen)
		
	
	def back_from_gr_options(self):
		"""
		Goes back to the first screen.
		"""
		
		self.layout.removeWidget(self.gr_options_screen)
		self.gr_options_screen.deleteLater()
		self.load_selection_screen()
		
		
	def gr_import(self):
		"""
		Starts importing proccess and closes this window.
		"""
		
		self.main_window.import_from_gr(self.gr_naming_selection, self.gr_additional_authors_selection)
		self.close()

	
	def load_merge_import_options_screen(self):
		"""
		Layout for importing options, after user choose to merge
		libraries.
		"""
		
		merge_back_button = QPushButton("Back")
		merge_back_button.clicked.connect(self.back_from_merge_options)
		
		merge_import_button = QPushButton("Import")
		merge_import_button.clicked.connect(self.merge_import)
		
		merge_options_buttons_layout = QHBoxLayout()
		merge_options_buttons_layout.addStretch()
		merge_options_buttons_layout.addWidget(self.cancel_button)
		merge_options_buttons_layout.addWidget(merge_back_button)
		merge_options_buttons_layout.addWidget(merge_import_button)
		
		merge_options_screen_layout = QVBoxLayout()
		merge_options_screen_layout.addWidget(QLabel('Click on "Import" to merge other library file created with this application into currently open library', wordWrap=True))
		merge_options_screen_layout.addStretch()
		merge_options_screen_layout.addLayout(merge_options_buttons_layout)
		
		self.merge_options_screen = QWidget()
		self.merge_options_screen.setLayout(merge_options_screen_layout)
		self.layout.addWidget(self.merge_options_screen)
		
		
	def back_from_merge_options(self):
		"""
		Goes back to the first screen.
		"""
		
		self.layout.removeWidget(self.merge_options_screen)
		self.merge_options_screen.deleteLater()
		self.load_selection_screen()
		
		
	def merge_import(self):
		"""
		Starts importing proccess and closes this window.
		"""
		
		self.main_window.merge_libraries()
		self.close()

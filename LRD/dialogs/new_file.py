from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
	QDialog,
	QHBoxLayout, 
	QLabel,
	QPushButton, 
	QVBoxLayout,
	)


class ConfirmNewLibrary(QDialog):
	"""
	If there are unsaved changes when user tries to start a new or open 
	another library, asks if user wants to save, discard changes or stay 
	using current library.
	
	Dialog composition: message and buttons "Save", "Discard" and 
	"Cancel".
	
	Buttons:
	Save: calls <main_window.save_as>. If the library isn't 
	saved, user will be prompted again.
	Discard: changes won't be saved.
	Cancel: closes this dialog without doing anything.
	
	args:
	main_window: parent reference to allow the use of its methods.
	behavior: either "new" or "open". Message and actions will be 
	adjusted accordingly.
	"""
	
	def __init__(self, main_window, behavior):
		super().__init__()
		self.main_window = main_window
		self.behavior = behavior
		
		self.resize(300, 100)
		self.setWindowIcon(QIcon('icons/save.png'))
		self.setWindowFlags(Qt.WindowCloseButtonHint)
		self.setWindowModality(Qt.ApplicationModal)
		self.setWindowTitle("Save changes")
		
		save_button = QPushButton("Save")
		save_button.clicked.connect(self.clicked_save)
		
		discard_button = QPushButton("Don't save")
		discard_button.clicked.connect(self.clicked_discard)
		
		cancel_button = QPushButton("Cancel")
		cancel_button.clicked.connect(self.close)
		
		buttons_area = QHBoxLayout()
		buttons_area.addWidget(save_button)
		buttons_area.addWidget(discard_button)
		buttons_area.addWidget(cancel_button)
		
		layout = QVBoxLayout(self)
		if self.behavior == 'new':
			layout.addWidget(QLabel("You are about to start a new library file, all<br></br> \
				unsaved changes on the current library will be lost"))
		elif self.behavior == 'open':
			layout.addWidget(QLabel("You are about to open another library file, all<br></br> \
				unsaved changes on the current library will be lost"))
		layout.addLayout(buttons_area)
		
		
	def clicked_save(self):
		"""
		On click button save: call main_window.save_as and check again
		for unsaved changes. If the saving process wasn't successful,
		user will be prompted again.
		"""
		
		self.main_window.save_as()
		if self.behavior == 'new':
			self.main_window.new_file()
		elif self.behavior == 'open':
			self.main_window.check_before_open_file()
		self.close()
		
		
	def clicked_discard(self):
		"""
		On click button discard: proceed to reset library or open 
		another library.
		"""
		
		if self.behavior == 'new':
			self.main_window.flag_unsaved_changes = False
			self.main_window.new_file()
		elif self.behavior == 'open':
			self.main_window.open_file()
		self.close()

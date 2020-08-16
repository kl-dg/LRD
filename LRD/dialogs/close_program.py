from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
	QDialog, 
	QHBoxLayout,
	QLabel,
	QPushButton, 
	QVBoxLayout,
	)
	

class AskSaveBeforeQuit(QDialog):
	"""
	If there are unsaved changes when user tries to close the program
	asks if user wants to save, discard changes or stay using it.
	
	Dialog composition: message and buttons "Save", "Discard" and 
	"Cancel".
	
	Buttons:
	Save: returns the answer 'save', which will lead to a call to
	main_window.save_as. If the saving proccess fails, this dialog will
	be shown again.
	
	Discard: returns the answer 'accept' to main_window.closeEvent(),
	causing the program to be closed without saving changes.
	
	Cancel: returns the answer 'ignore' to main_window.closeEvent().
	Changes won't be saved and the program won't be closed.
	
	args:
	main_window: parent reference to allow the use of its methods or
	attributes.
	"""
	
	def __init__(self, main_window):
		super().__init__()
		self.main_window = main_window
		self.setWindowModality(Qt.ApplicationModal)
		self.setWindowTitle("Save before quitting")
		self.resize(300, 100)
		self.setWindowFlags(Qt.WindowCloseButtonHint)
		
		save_button = QPushButton(self)
		save_button.setText("Save")
		save_button.clicked.connect(lambda: self.return_answer('save'))
		
		discard_button = QPushButton(self)
		discard_button.setText("Don't save")
		discard_button.clicked.connect(lambda: self.return_answer('accept'))
		
		cancel_button = QPushButton(self)
		cancel_button.setText("Cancel")
		cancel_button.clicked.connect(lambda: self.return_answer('ignore'))
		
		buttons_area = QHBoxLayout()
		buttons_area.addWidget(save_button)
		buttons_area.addWidget(discard_button)
		buttons_area.addWidget(cancel_button)
		
		layout = QVBoxLayout(self)
		layout.addWidget(QLabel("There are unsaved changes, save before exiting program?"))
		layout.addLayout(buttons_area)
		
		
	def return_answer(self, answer):
		"""
		Return user's choice to main_window.closeEvent.
		
		args:
		answer: event action on user's choice.
		"""
		
		self.main_window.answer_close = answer
		self.close()

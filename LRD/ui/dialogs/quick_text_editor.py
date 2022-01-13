from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QTextEdit, QVBoxLayout

from data.libraries import books
from control.edit_library import edit_text_attribute
from ui.main_window_proxy import main_window

class EditText(QDialog):
	"""
	Dialog with a text box for quickly editing review, quotes or notes.
	
	Dialog layout: text box followed by buttons to accept or discard.
	
	args:
	index: selected book's static library index.
	
	field: attribute to be edited, either 'review', 'quotes' or 'notes'.
	"""
	
	def __init__(self, index, field):
		super().__init__()
		self.index = index
		self.field = field
		
		self.resize(600, 600)
		self.setWindowFlags(Qt.WindowCloseButtonHint)
		self.setWindowModality(Qt.ApplicationModal)
		self.setWindowTitle(f"Edit {self.field.title()}")
		
		self.text_box = QTextEdit()
		self.text_box.setText(getattr(books[index], self.field))

		button_save = QPushButton(f"Save {self.field}")
		button_save.clicked.connect(self.clicked_save_text)
		
		button_discard = QPushButton("Discard changes")
		button_discard.clicked.connect(self.close)
		
		buttons = QHBoxLayout()
		buttons.addWidget(button_save)
		buttons.addWidget(button_discard)
		
		layout = QVBoxLayout(self)
		layout.addWidget(QLabel(f"{self.field.title()} on {books[index].title} by {'; '.join(books[index].author)}", wordWrap=True))
		layout.addWidget(self.text_box)		
		layout.addLayout(buttons)
		
		
	def clicked_save_text(self):
		"""
		Save edited review, quotes or notes.
		"""
		
		if getattr(books[self.index], self.field) != self.text_box.toPlainText():
			edit_text_attribute(self.index, self.field, self.text_box.toPlainText())
			main_window.flag_unsaved_changes = True
			main_window.set_interface_outdated()
			main_window.refresh_current_tab()

		self.close()

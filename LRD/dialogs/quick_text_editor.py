from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
	QDialog, 
	QHBoxLayout,
	QLabel, 
	QPushButton,
	QTextEdit, 
	QVBoxLayout, 
	)

from library.book_library import book_list

class EditText(QDialog):
	"""
	Dialog with a text box for quickly editing review, quotes or notes.
	
	Dialog layout: text box followed by buttons to accept or discard.
	
	args:
	index: selected book's static library index.
	
	field: attribute to be edited, either 'review', 'quotes' or 'notes'.
	"""
	
	def __init__(self, index, field, parent):
		super().__init__()
		self.index = index
		self.field = field
		self.parent = parent
		
		self.resize(600, 600)
		self.setWindowFlags(Qt.WindowCloseButtonHint)
		self.setWindowModality(Qt.ApplicationModal)
		self.setWindowTitle(f"Edit {self.field.title()}")
		
		self.text_box = QTextEdit()
		self.text_box.setText(getattr(book_list[index], self.field))

		button_save = QPushButton(f"Save {self.field}")
		button_save.clicked.connect(self.save_text)
		
		button_discard = QPushButton("Discard changes")
		button_discard.clicked.connect(self.close)
		
		buttons = QHBoxLayout()
		buttons.addWidget(button_save)
		buttons.addWidget(button_discard)
		
		layout = QVBoxLayout(self)
		layout.addWidget(QLabel(f"{self.field.title()} on {book_list[index].title} by {'; '.join(book_list[index].author)}", wordWrap=True))
		layout.addWidget(self.text_box)		
		layout.addLayout(buttons)
		
		
	def save_text(self):
		"""
		Save edited review, quotes or notes.
		"""
		
		setattr(book_list[self.index], self.field, self.text_box.toPlainText())
		self.parent.flag_unsaved_changes = True
		self.parent.set_interface_outdated()
		self.close()

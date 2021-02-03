from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
	QDialog, 
	QHBoxLayout,
	QLineEdit, 
	QPushButton, 
	QVBoxLayout,
	)

from library.book_library import library


class EditValueByAttribute(QDialog):
	"""
	Batch edits all books that share an attribute value.
	
	Dialog composition: one line text field and buttons OK ("Edit") and 
	"Cancel". 
	
	args:
	value: string to be edited such as Publisher's or Author's name.
	attribute: what book attribute e.g. "author", "publisher", "series".
	"""
	
	def __init__(self, value, attribute, main_window):
		super().__init__()
		self.value = value
		self.attribute = attribute
		self.main_window = main_window
		
		self.resize(200, 80)
		self.setWindowFlags(Qt.WindowCloseButtonHint)
		self.setWindowModality(Qt.ApplicationModal)
		self.setWindowTitle(f"Edit {self.attribute.title()}")

		self.text_field = QLineEdit()
		self.text_field.setText(self.value)
		
		button_edit = QPushButton(self)
		button_edit.setText("Edit")
		button_edit.clicked.connect(self.clicked_edit)
		
		button_cancel = QPushButton(self)
		button_cancel.setText("Cancel")
		button_cancel.clicked.connect(self.close)
		
		buttons_area = QHBoxLayout()
		buttons_area.addWidget(button_edit)
		buttons_area.addWidget(button_cancel)
		
		layout = QVBoxLayout(self)
		layout.addWidget(self.text_field)
		layout.addLayout(buttons_area)


	def clicked_edit(self):
		"""
		If value was changed by user, find matching ocurrences and 
		replace by the new value.
		"""
		
		if self.value != self.text_field.text().strip():
			if self.attribute == 'author':
				for book in library.values():
					if self.value in book.author:
						if len(self.text_field.text().strip()) == 0:
							ocurrences_indexes = [i for i in range(len(book.author)) if book.author[i] == self.value]
							ocurrences_indexes.sort(reverse=True)
							for i in ocurrences_indexes:
								book.author.pop(i)
						else:
							book.author = [self.text_field.text().strip() if author == self.value else author for author in book.author]
			
			else:
				for book in library.values():
					if getattr(book, self.attribute) == self.value:
						setattr(book, self.attribute, self.text_field.text().strip())
		
			self.main_window.flag_unsaved_changes = True
			self.main_window.set_interface_outdated()
			
		self.close()

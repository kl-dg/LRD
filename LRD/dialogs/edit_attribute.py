from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout

from library.edit_library import edit_attribute_value
from main_ui.main_window_proxy import main_window


class EditValueByAttribute(QDialog):
	"""
	Batch edits all books that share an attribute value.
	
	Dialog composition: one line text field and buttons OK ("Edit") and 
	"Cancel". 
	
	args:
	value: string to be edited such as Publisher's or Author's name.
	attribute: what book attribute e.g. "author", "publisher", "series".
	"""
	
	def __init__(self, value, attribute):
		super().__init__()
		self.value = value
		self.attribute = attribute
		
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
			edit_attribute_value(self.value, self.text_field.text().strip(), self.attribute)
		
			main_window.flag_unsaved_changes = True
			main_window.set_interface_outdated()
			
		self.close()

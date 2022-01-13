from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout

from data.libraries import books

class DeleteBook(QDialog):
	"""
	Asks user for confirmation whether they want to delete the selected
	book.
	Dialog composition: questioning message, buttons "OK" and "Cancel".
	
	args:
	self.index: book's index in the library.
	"""
	
	def __init__(self, index):
		super().__init__()
		self.setMinimumWidth(400)
		self.setWindowIcon(QIcon('icons/delete.png'))
		self.setWindowFlags(Qt.WindowCloseButtonHint)
		self.setWindowModality(Qt.ApplicationModal)
		self.setWindowTitle("Delete Book")
		
		message = QLabel(f"Are you sure you want to delete <b>{books[index].title}</b> by <b>{'; '.join(books[index].author)}</b>? <br><\br><br><\br>This action cannot be undone.<br><\br>", wordWrap=True)
		
		buttons = QDialogButtonBox(
			QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
			Qt.Horizontal, 
			self)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)
			
		layout = QVBoxLayout(self)
		layout.addWidget(message)
		layout.addWidget(buttons)

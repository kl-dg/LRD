from PyQt5.QtWidgets import QWidget

class EmptyPanel(QWidget):
	"""
	Information panel when there's no selected book.
	"""
	
	def __init__(self):
		super().__init__()
		self.setMaximumWidth(400)
		self.setMinimumWidth(400)

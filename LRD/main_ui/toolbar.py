from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QToolBar

class ToolBar(QToolBar):
	"""
	Main window toolbar layout.
	
	args:
	main_window: parent reference to access its methods.
	"""
	
	def __init__(self, main_window):
		super().__init__()
		self.setIconSize(QSize(48, 48))
		self.setMovable(False)
		self.setStyleSheet("QToolButton{padding-right: 15px}")
		self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		
		button_new = QAction(self)
		button_new.setIcon(QIcon('icons/new.png'))
		button_new.setIconText("New Library")
		button_new.triggered.connect(main_window.new_file)
		
		button_open = QAction(self)
		button_open.setIcon(QIcon('icons/open.png'))
		button_open.setIconText("Open")
		button_open.triggered.connect(main_window.check_before_open_file)
		
		button_save = QAction(self)
		button_save.setIcon(QIcon('icons/save.png'))
		button_save.setIconText("Save")
		button_save.triggered.connect(main_window.save_file)
		
		button_save_as = QAction(self)
		button_save_as.setIcon(QIcon('icons/save_as.png'))
		button_save_as.setIconText("Save As")
		button_save_as.triggered.connect(main_window.save_as)
		
		button_add = QAction(self)
		button_add.setIcon(QIcon('icons/add.png'))
		button_add.setIconText("Add Book")
		button_add.triggered.connect(main_window.add_book)
		
		button_edit = QAction(self)
		button_edit.setIcon(QIcon('icons/edit.png'))
		button_edit.setIconText("Edit")
		button_edit.triggered.connect(main_window.edit_book)
		
		button_delete = QAction(self)
		button_delete.setIcon(QIcon('icons/delete.png'))
		button_delete.setIconText("Delete")
		button_delete.triggered.connect(main_window.delete_book)
		
		button_import = QAction(self)
		button_import.setIcon(QIcon('icons/import.png'))
		button_import.setIconText("Import")
		button_import.triggered.connect(main_window.open_import_assistant)
		
		self.addAction(button_new)
		self.addAction(button_open)
		self.addAction(button_save)
		self.addAction(button_save_as)
		self.addSeparator()
		self.addAction(button_add)
		self.addAction(button_edit)
		self.addAction(button_delete)
		self.addSeparator()
		self.addAction(button_import)
		
		

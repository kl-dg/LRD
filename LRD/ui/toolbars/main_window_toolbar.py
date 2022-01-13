from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QToolBar

from ui.main_window_proxy import main_window

class MainWindowToolBar(QToolBar):
	"""
	Main window toolbar layout.
	"""
	
	def __init__(self):
		super().__init__()
		self.setIconSize(QSize(48, 48))
		self.setMovable(False)
		self.setStyleSheet("QToolButton{padding-right: 15px}")
		self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		
		button_new = QAction(self)
		button_new.setIcon(QIcon('assets/icons/new.png'))
		button_new.setIconText("New Library")
		#For some reason QAction.triggered signal will send checked = False argument if connected to a proxy, nothing
		#if connected to QMainWindow. Lambda will prevent called method from receiving this unnecessary argument.
		button_new.triggered.connect(lambda: main_window.new_file())
		
		button_open = QAction(self)
		button_open.setIcon(QIcon('assets/icons/open.png'))
		button_open.setIconText("Open")
		button_open.triggered.connect(lambda: main_window.check_before_open_file())
		
		button_save = QAction(self)
		button_save.setIcon(QIcon('assets/icons/save.png'))
		button_save.setIconText("Save")
		button_save.triggered.connect(lambda: main_window.save_file())
		
		button_save_as = QAction(self)
		button_save_as.setIcon(QIcon('assets/icons/save_as.png'))
		button_save_as.setIconText("Save As")
		button_save_as.triggered.connect(lambda: main_window.save_as())
		
		button_add = QAction(self)
		button_add.setIcon(QIcon('assets/icons/add.png'))
		button_add.setIconText("Add Book")
		button_add.triggered.connect(lambda: main_window.add_book())
		
		button_edit = QAction(self)
		button_edit.setIcon(QIcon('assets/icons/edit.png'))
		button_edit.setIconText("Edit")
		button_edit.triggered.connect(lambda: main_window.edit_book())
		
		button_delete = QAction(self)
		button_delete.setIcon(QIcon('assets/icons/delete.png'))
		button_delete.setIconText("Delete")
		button_delete.triggered.connect(lambda: main_window.clicked_delete_book())
		
		button_import = QAction(self)
		button_import.setIcon(QIcon('assets/icons/import.png'))
		button_import.setIconText("Import")
		button_import.triggered.connect(lambda: main_window.open_import_assistant())
		
		#Add buttons to toolbar
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

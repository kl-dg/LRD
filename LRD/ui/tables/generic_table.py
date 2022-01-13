from PyQt5.QtWidgets import QAbstractItemView, QTableWidget

class GenericTable(QTableWidget):
	"""
	Creates a class of tables with row selection, non-editable, 
	single selection, 10pt row height and no vertical headers.
	"""
	
	def __init__(self, column_count):
		super().__init__()
		self.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.setSelectionMode(QAbstractItemView.SingleSelection)
		self.verticalHeader().setDefaultSectionSize(10)
		self.verticalHeader().hide()
		self.horizontalHeader().sectionClicked.connect(self.click_sort)
		self.setRowCount(0)
		self.setColumnCount(column_count)
		
		
	def click_sort(self, index):
		"""
		Gets user click on column header and calls <refresh_table>
		
		args:
		index: column header clicked by user.
		"""
		
		if f'{index}' == self.current_sorting: 
			self.current_sorting = f'{index}r'
		else: self.current_sorting = f'{index}'
		self.refresh_table(sorting=True)

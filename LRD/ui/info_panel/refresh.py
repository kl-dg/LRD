from ui.info_panel.empty_panel import EmptyPanel
from ui.info_panel.info_panel import InfoPanel


def refresh_panel(tab):
	"""
	Display information on book selected by user.
	
	args: 
	tab: main_window tab where it should be inserted to.
	"""
	
	try:
		if tab.selected_book is not None:
			reset_panel(tab)
			tab.panel = EmptyPanel()
			tab.panel_form = InfoPanel(tab.selected_book)
			tab.panel.setLayout(tab.panel_form)
			tab.layout.addWidget(tab.panel)
			return
	except (KeyError, IndexError): pass
	reset_panel(tab)
	tab.panel = EmptyPanel()
	tab.layout.addWidget(tab.panel)


def reset_panel(tab):
	"""
	Removes Info Panel when redrawing it.
	
	args: 
	tab: main_window tab where it should be removed from.
	"""
	
	if tab.panel is not None:
		tab.layout.removeWidget(tab.panel)
		#deleteLater() removes subwidgets, preventing overlapping
		tab.panel.deleteLater()

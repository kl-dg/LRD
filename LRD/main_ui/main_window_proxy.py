class MainWindowProxy:
	"""
	Creates a proxy for main window.
	
	All UI actions are attached to main window, this proxy will save the trouble of referencing main window as a
	parameter all the way down to the widgets.
	
	See use below.
	"""
	
	def __init__(self):
		self.wrapped_object = None
		
	def __getattr__(self, method):
		return getattr(self.wrapped_object, method)

#Use: set main_window.wrapped_object attribute to the actual main window object.
main_window = MainWindowProxy()

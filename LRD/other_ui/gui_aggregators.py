from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

def matplotlib_pyqt_agg(figure):
	"""
	Allows a matplotlib figure to be added to a PyQt GUI.
	
	FigureCanvasQTAgg.setMinimumSize preserves figure proportions inside a scrollable widget. If
	this is not needed, this function may be skipped and FigureCanvasQTAgg called directly.
	
	Parameter:
	
	figure: a matplotlib Figure object.
	
	Returns: a FigureCanvasQTAgg object, which can be added to a PyQt GUI.
	"""
	
	qt_figure = FigureCanvasQTAgg(figure)
	qt_figure.setMinimumSize(qt_figure.size())

	return qt_figure

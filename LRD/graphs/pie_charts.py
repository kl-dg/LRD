from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

def books_in_series_vs_standalone_pie_chart(in_series, standalone):
	"""
	Generates a matplotlib pie chart displaying proportion of books in
	series versus standalone books.
	
	Parameters: 
	in_series: amount of books with a non-empty series attribute.
	
	standalone: amount of books with an empty series attribute.
	
	Return: a FigureCanvasQTAgg object containing the plotted chart ready to be 
	added to a PyQt GUI.
	"""
	
	#Create matplotlib figure
	figure = Figure(figsize=(8,5))
	
	#Create pie chart
	pie_chart = figure.add_subplot(111)
	pie_chart.set_title("Books in series vs. standalone")
	pie_chart.axis('equal')
	pie_chart.pie(
		(in_series, standalone), 
		labels = ("Series", "Standalone"), 
		autopct='%1.1f%%', 
		shadow = True
		)
	
	#Create Qt compatible figure
	qt_figure = FigureCanvasQTAgg(figure)
	qt_figure.setMinimumSize(qt_figure.size())

	return qt_figure

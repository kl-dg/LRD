from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

def books_by_length_histogram(bin_list):
	"""
	Generates a matplotlib vertical bar chart displaying the distribution
	of book length (in pages).
	
	Parameter:
	bin_list: must be a list of eleven integers, representing book counts for each
	100-pages bin between 0 and 999 pages, plus a bin for longer books (1000+ pages).
	
	Return: a FigureCanvasQTAgg object containing the plotted chart ready to be 
	added to a PyQt GUI.
	"""
	
	#Create a matplotlib figure
	figure = Figure(figsize=(8,7))
	
	#Create bar chart
	bar_chart = figure.add_subplot(111)
	bar_chart.bar((
		"0 - 99", 
		"100 - 199", 
		"200 - 299", 
		"300 - 399", 
		"400 - 499", 
		"500 - 599", 
		"600 - 699", 
		"700 - 799", 
		"800 - 899", 
		"900 - 999", 
		"1000 +"
		), 
		bin_list, 
		zorder=3)
		
	bar_chart.yaxis.grid(True, linestyle=':', zorder=0, alpha=0.3)
	bar_chart.tick_params('x', labelrotation = 50)
	bar_chart.set_title("Books by number of pages")
	
	#Value labels
	for index, value in enumerate(bin_list):
		bar_chart.text(
			index - len(str(value)) * 0.1 + 0.05,
			value + 0.01 * max(bin_list),
			str(value),
			color='tab:blue',
			fontweight='bold', 
			size=9
			)
		
	#Create Qt compatible figure
	qt_figure = FigureCanvasQTAgg(figure)
	qt_figure.setMinimumSize(qt_figure.size())
	
	return qt_figure

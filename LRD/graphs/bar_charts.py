from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from functions.value_calculations import bar_chart_text_pos_h

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


def books_by_rating_vbar_chart(count_array):
	"""
	Generates a matplotlib vertical bar chart displaying the distribution
	of book ratings.
	
	Parameter:
	count_array: must be a list of five integers, index zero for one star to index four for
	five stars count.
	
	Return: a FigureCanvasQTAgg object containing the plotted chart ready to be 
	added to a PyQt GUI.
	"""
	
	#Create a matplotlib figure
	figure = Figure(figsize=(8,5))
	
	#Create bar chart
	bar_chart = figure.add_subplot(111)
	bar_chart.bar(("1 star", "2 stars", "3 stars", "4 stars", "5 stars"), count_array, zorder=3)
	bar_chart.yaxis.grid(True, linestyle=':', zorder=0, alpha=0.3)
	bar_chart.set_title("Rating distribution")
	
	#Value labels
	for index, value in enumerate(count_array):
		bar_chart.text(
			index - 0.1,
			value + 0.01 * max(count_array),
			str(value),
			color='tab:blue',
			fontweight='bold', 
			size=9
			)
	
	#Create Qt compatible figure
	qt_figure = FigureCanvasQTAgg(figure)
	qt_figure.setMinimumSize(qt_figure.size())
	
	return qt_figure
	
	
def horizontal_bar_chart(labels, values, title):
	"""
	Generates a customable matplotlib horizontal bar chart.
	
	Parameters:
	labels: a list of bars labels.
	
	values: a numerical list. Each value must be at same index of its label.
	
	title: chart's title.
	
	Return: a FigureCanvasQTAgg object containing the plotted chart ready to be 
	added to a PyQt GUI.
	"""
	
	#Create a matplotlib figure
	figure = Figure(figsize=(8,len(labels)/3))
	
	#Create bar chart
	bar_chart = figure.add_subplot(111)
	bar_chart.barh(labels, values, zorder=3)
	bar_chart.xaxis.grid(True, linestyle=':', zorder=0, alpha=0.3)
	bar_chart.set_title(title)
	
	max_value = max(values)
	
	#Value labels
	for index, value in enumerate(values):
		if value < max_value / 10:
			bar_chart.text(
				value, 
				index, 
				" "+str(value),
				va='center', 
				color='tab:blue', 
				fontweight='bold', 
				size=9
				)
				
		elif value >= max_value / 10:
			bar_chart.text(
				bar_chart_text_pos_h(value, max_value),
				index, 
				str(value),
				va='center', 
				color='white', 
				fontweight='bold', 
				size=9
				)
		
	#Create Qt compatible figure
	qt_figure = FigureCanvasQTAgg(figure)
	qt_figure.setMinimumSize(qt_figure.size())
	
	return qt_figure

from matplotlib.figure import Figure

class PieChartBooksByFormat(Figure):

	"""
	Generates a matplotlib pie chart displaying proportion of books by format
	(physical, ebook or audiobook).
	
	Parameter:
	chart_data: must be a dictionary with two keys: 'labels' and 'counts', their values
	must be two lists including only formats which book count is greater than zero. Labels
	and their respective counts must be at the same index.
	"""

	def __init__(self, chart_data):
		super().__init__(figsize=(8,5))

		chart = self.add_subplot(111)
		chart.pie(chart_data['counts'], labels=chart_data['labels'], autopct='%1.1f%%', shadow = True)
		chart.set_title("Books by format")
		chart.axis('equal')

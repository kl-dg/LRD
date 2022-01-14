from matplotlib.figure import Figure

class PieChartBooksByReadingStatus(Figure):

	"""
	Generates a matplotlib pie chart displaying proportion of books by reading status.
	
	Parameter:
	chart_data: must be a dictionary with two keys: 'labels' and 'counts', their values
	must be two lists including only statuses which book count is greater than zero. Labels
	and their respective counts must be at the same index.
	"""

	def __init__(self, chart_data):
		super().__init__(figsize=(8,5))

		chart = self.add_subplot(111)
		chart.pie(chart_data['counts'], labels = chart_data['labels'], autopct='%1.1f%%', shadow = True)
		chart.set_title("Library composition by reading status")
		chart.axis('equal')
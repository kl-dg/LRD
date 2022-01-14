from matplotlib.figure import Figure

class PieChartBooksInSeriesVsStandalone(Figure):

	"""
	Generates a matplotlib pie chart displaying proportion of books in
	series versus standalone books.
	
	Parameters: 
	in_series: amount of books with a non-empty series attribute.
	
	standalone: amount of books with an empty series attribute.
	"""

	def __init__(self, in_series, standalone):
		super().__init__(figsize=(8,5))

		#Create pie chart
		chart = self.add_subplot(111)
		chart.set_title("Books in series vs. standalone")
		chart.axis('equal')
		chart.pie(
			(in_series, standalone), 
			labels = ("Series", "Standalone"), 
			autopct='%1.1f%%', 
			shadow = True
			)

from matplotlib.figure import Figure

class VBarChartBooksByRating(Figure):
	"""
	Generates a matplotlib vertical bar chart displaying the distribution
	of book ratings.
	
	Parameter:
	count_array: must be a list of five integers, index zero for one star to index four for
	five stars count.
	"""

	def __init__(self, count_array):
		super().__init__(figsize=(8,5))

		#Create bar chart
		chart = self.add_subplot(111)
		chart.bar(("1 star", "2 stars", "3 stars", "4 stars", "5 stars"), count_array, zorder=3)
		chart.yaxis.grid(True, linestyle=':', zorder=0, alpha=0.3)
		chart.set_title("Rating distribution")
	
		#Value labels
		for index, value in enumerate(count_array):
			chart.text(
				index - 0.1,
				value + 0.01 * max(count_array),
				str(value),
				color='tab:blue',
				fontweight='bold', 
				size=9
				)

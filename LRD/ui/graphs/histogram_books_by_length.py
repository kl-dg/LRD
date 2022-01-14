from matplotlib.figure import Figure

class HistogramBooksByLength(Figure):
	"""
	Generates a matplotlib vertical bar chart displaying the distribution
	of book length (in pages).
	
	Parameter:
	bin_list: must be a list of eleven integers, representing book counts for each
	100-pages bin between 0 and 999 pages, plus a bin for longer books (1000+ pages).
	"""
	
	def __init__(self, bin_list):
		super().__init__(figsize=(8,7))

		#Create bar chart
		chart = self.add_subplot(111)
		chart.bar((
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
		
		chart.yaxis.grid(True, linestyle=':', zorder=0, alpha=0.3)
		chart.tick_params('x', labelrotation = 50)
		chart.set_title("Books by number of pages")
	
		#Value labels
		for index, value in enumerate(bin_list):
			chart.text(
				index - len(str(value)) * 0.1 + 0.05,
				value + 0.01 * max(bin_list),
				str(value),
				color='tab:blue',
				fontweight='bold', 
				size=9
				)
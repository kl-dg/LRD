from matplotlib.figure import Figure

from functions.value_calculations import bar_chart_text_pos_h


class HorizontalBarChart(Figure):
	"""
	Generates a customable matplotlib horizontal bar chart.
	
	Parameters:
	labels: a list of bars labels.
	
	values: a numerical list. Each value must be at same index of its label.
	
	title: chart's title.
	"""

	def __init__(self, labels, values, title):
		super().__init__(figsize=(8,len(labels)/3))

		#Create bar chart
		chart = self.add_subplot(111)
		chart.barh(labels, values, zorder=3)
		chart.xaxis.grid(True, linestyle=':', zorder=0, alpha=0.3)
		chart.set_title(title)
	
		max_value = max(values)
	
		#Value labels
		for index, value in enumerate(values):
			if value < max_value / 10:
				chart.text(
					value, 
					index, 
					" "+str(value),
					va='center', 
					color='tab:blue', 
					fontweight='bold', 
					size=9
					)
				
			elif value >= max_value / 10:
				chart.text(
					bar_chart_text_pos_h(value, max_value),
					index, 
					str(value),
					va='center', 
					color='white', 
					fontweight='bold', 
					size=9
					)

def average(value, count):
	"""
	Performs a division operation, return a 0 if it's going to cause
	a ZeroDivisionError.
	"""
	
	if count == 0: return 0
	else: return value / count


def bar_chart_text_pos_h(value, max_value, distance=0.015):
	"""
	Measure label position on matplotlib bar chart.
	"""
	
	len_value = len(str(value))
	difference = distance * len_value * max_value
	return value - difference

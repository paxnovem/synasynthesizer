def array_one_to_two(original_list, wrap_amount):
	position = 0
	line_number = 0
	return_list = []
	
	for line_number in original_list:
		new_list =  original_list[position : position + wrap_amount]
		if(not new_list):
			break
		return_list.append(new_list)
		position = position + wrap_amount
		
	return return_list

def brightest_points_in_list(two_list):
	pass	
	
def delta_from_baseline(baseline_data, current_data):
	list_of_deltas = []
	for row_number in range(len(current_data)):
		row = current_data[row_number]
		new_row = []
		for column_number in range(len(row)):
			current_cell = row[column_number]
			baseline_current_cell = baseline_data[row_number][column_number]
			delta_of_current_cell = current_cell - baseline_current_cell
			new_row.append(delta_of_current_cell)
		list_of_deltas.append(new_row)
	
	return list_of_deltas		

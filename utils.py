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

def find_touch_area(delta_list, point, buffer, visited_list):
	if point in visited_list:
		return None
	visited_list.append(point)	
	y, x = point
	delta = delta_list[y][x]
	if delta <= buffer:
		return None
	column_count = len(delta_list[0])
	if x > 0:
		west_point = (y, x - 1)
	if y > 0:
		north_point = (y - 1, x)
		if x > 0:
			pass
		if y < len(visited_list) - 2:
			pass
	if y < len(visited_list) - 2:
		east_point = (y, x + 1)
		if x > 0:
			pass
		if x < column_count - 2:
			pass	
	if x < column_count - 2:
		south_point = (y + 1, x)
	
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

baseline_data = [
	[5, 5, 5, 5, 5, 5, 5],
	[5, 5, 5, 5, 5, 5, 5],
	[5, 5, 5, 5, 5, 5, 5],
	[5, 5, 5, 5, 5, 5, 5],
	[5, 5, 5, 5, 5, 5, 5],
	[5, 5, 5, 5, 5, 5, 5],
	[5, 5, 5, 5, 5, 5, 5],
]

test_data = [
	[5, 9, 5, 5, 5, 5, 5],
	[9, 9, 9, 5, 5, 5, 5],
	[9, 5, 9, 5, 5, 5, 5],
	[5, 9, 5, 5, 9, 9, 9],
	[5, 5, 5, 5, 5, 9, 5],
	[5, 5, 5, 5, 9, 9, 9],
	[5, 5, 5, 5, 5, 9, 9],
]

buffer = 2

delta_list = delta_from_baseline(baseline_data, test_data)
print(delta_list)

visited_list = []

for row_number in range(len(delta_list)):
	row = delta_list[row_number]
	for column_number in range(len(row)):
		point = (row_number, column_number)
		touch_area = find_touch_area(delta_list, point, visited_list)

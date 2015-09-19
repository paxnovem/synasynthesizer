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
	

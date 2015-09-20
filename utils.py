def array_one_to_two(original_list, wrap_amount):
    position = 0
    line_number = 0
    return_list = []

    for line_number in original_list:
        new_list =  original_list[position : position + wrap_amount]
        if not new_list:
            break
        return_list.append(new_list)
        position = position + wrap_amount

    return return_list

def find_touch_area(delta_list, point, buffer, visited_list):
    if point in visited_list:
        return None

    y, x = point
    delta = delta_list[y][x]

    if delta <= buffer:
        return None

    visited_list.append(point)

    row_count = len(delta_list)
    column_count = len(delta_list[0])

    if x > 0:
        west_point = (y, x - 1)
        find_touch_area(
            delta_list, west_point, buffer, visited_list
        )

    if x < column_count - 1:
        east_point = (y, x + 1)
        find_touch_area(
            delta_list, east_point, buffer, visited_list
        )

    if y > 0:
        north_point = (y - 1, x)
        find_touch_area(
            delta_list, north_point, buffer, visited_list
        )

        if x > 0:
            northwest_point = (y - 1, x - 1)
            find_touch_area(
                delta_list, northwest_point, buffer, visited_list
            )

        if x < column_count - 1:
            northeast_point = (y - 1, x + 1)
            find_touch_area(
                delta_list, northeast_point, buffer, visited_list
            )
    if y < row_count - 1:
        south_point = (y + 1, x)
        find_touch_area(
            delta_list, south_point, buffer, visited_list
        )

        if x > 0:
            southwest_point = (y + 1, x - 1)
            find_touch_area(
                delta_list, southwest_point, buffer, visited_list
            )
        if x < column_count - 1:
            southeast_point = (y + 1, x + 1)
            find_touch_area(
                delta_list, southeast_point, buffer, visited_list
            )


def touch_area_from_visited(visited_list):
    if not visited_list:
        return None

    area_x1 = visited_list[0][0]
    area_y1 = visited_list[0][1]

    area_x2 = visited_list[0][0]
    area_y2 = visited_list[0][1]

    for x, y in visited_list:
        if x < area_x1:
            area_x1 = x

        if y < area_y1:
            area_y1 = y

        if x > area_x2:
            area_x2 = x

        if y > area_y2:
            area_y2 = y

    return (area_x1, area_y1, area_x2, area_y2)


def touch_area_midpoint(touch_x1, touch_y1, touch_x2, touch_y2):
    area_x = (touch_x1 + touch_x2) // 2
    area_y = (touch_y1 + touch_y2) // 2

    return (area_x, area_y)


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
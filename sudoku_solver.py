import math
from typing import DefaultDict
from pprint import pprint
import time
import copy

QUADRANT_LENGTH = 3
CONTAINER_LENGTH = QUADRANT_LENGTH ** 2


NUMBERS = tuple(range(1, CONTAINER_LENGTH + 1))
GRID53 = [
    [0, 6, 7, 0, 0, 8, 0, 0, 0],
    [1, 0, 0, 0, 9, 0, 4, 0, 0],
    [0, 0, 0, 1, 0, 6, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 7, 0, 5],
    [5, 0, 0, 9, 7, 0, 0, 0, 3],
    [0, 0, 0, 0, 4, 0, 9, 1, 0],
    [0, 0, 3, 0, 0, 0, 1, 8, 0],
    [0, 0, 0, 0, 0, 1, 0, 9, 0],
    [0, 0, 0, 5, 0, 0, 0, 0, 6],
]
GRID149 = [
    [0, 6, 0, 3, 0, 1, 0, 0, 4],
    [0, 0, 0, 0, 0, 0, 0, 9, 0],
    [0, 0, 2, 5, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 3, 9, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 6, 5],
    [0, 4, 0, 0, 7, 0, 8, 0, 0],
    [0, 0, 0, 0, 0, 5, 0, 3, 0],
    [0, 2, 5, 8, 0, 6, 0, 7, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 0],
]

GRID150 = [
    [0, 0, 0, 0, 4, 2, 9, 5, 0],
    [0, 8, 0, 0, 0, 1, 0, 0, 0],
    [7, 0, 0, 3, 0, 0, 0, 0, 4],
    [8, 0, 5, 0, 3, 0, 0, 0, 1],
    [0, 3, 0, 0, 0, 0, 0, 8, 0],
    [0, 2, 0, 5, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 4, 0, 0],
    [5, 0, 0, 0, 7, 0, 6, 0, 3],
    [9, 0, 0, 0, 0, 0, 0, 0, 0],
]

GRID = GRID149


def get_quadrant_row_start(row, base=QUADRANT_LENGTH):
    """get the starting number of each row"""
    return base * math.floor(row / base)


def get_row_from_quad_index(index):
    return get_quadrant_row_start(index)


def get_col_from_quad_index(index):
    return (index % QUADRANT_LENGTH) * QUADRANT_LENGTH


def get_quadrant_col(col, base=QUADRANT_LENGTH):
    """get the quadrant value to add on to each row start"""
    return math.floor(col / base)


def get_quadrant_index(row, col):
    """
    quadrant values start at zero in upper left and increase by 1 going across the first row
    [
        0,1,2,
        3,4,5,
        6,7,8
    ]
    """
    quadrant_row_start = get_quadrant_row_start(row)
    quadrant_col = get_quadrant_col(col)
    return quadrant_row_start + quadrant_col


def add_to_container(container_dict, index, value):
    if value == 0 or value == False:
        return
    container_dict[index].append(value)


def in_container(container_dict, index, value):
    if value in container_dict[index]:
        return True


def update_containers(containers, grid=GRID):
    for row, row_list in enumerate(grid):
        for col, value in enumerate(row_list):
            add_to_container(containers["rows"], row, value)
            add_to_container(containers["cols"], col, value)
            quad_index = get_quadrant_index(row, col)
            # print(quad_index)
            add_to_container(containers["quads"], quad_index, value)


def build_false_grid(grid_size=CONTAINER_LENGTH):
    grid = []
    for row in range(grid_size):
        row = []
        for col in range(grid_size):
            row.append(False)
        grid.append(row)
    return grid


def get_slice_and_dice_grid(containers, target_number, grid=GRID):
    """
    slice and dice grid is a boolean representation of where the target number can't be
    blocked positions are represented by True
    """
    slice_and_dice_grid = build_false_grid()
    for row, row_list in enumerate(grid):
        for col, value in enumerate(row_list):
            if value != 0:
                slice_and_dice_grid[row][col] = True
                continue
            if in_container(containers["rows"], row, target_number):
                slice_and_dice_grid[row][col] = True
                continue
            if in_container(containers["cols"], col, target_number):
                slice_and_dice_grid[row][col] = True
                continue
            quad_index = get_quadrant_index(row, col)
            if in_container(containers["quads"], quad_index, target_number):
                slice_and_dice_grid[row][col] = True
                continue
    return slice_and_dice_grid


def get_quadrant_row_range(index):
    first_row = get_row_from_quad_index(index)
    last_row = first_row + QUADRANT_LENGTH
    return tuple(range(first_row, last_row))


def get_quadrant_col_range(index):
    first_col = get_col_from_quad_index(index)
    last_col = first_col + QUADRANT_LENGTH
    return tuple(range(first_col, last_col))


def fill_hole_in_range(row_range, col_range, hole_grid, number, grid=GRID):
    """this is where the hole is actuall filled in the grid"""
    for row in row_range:
        for col in col_range:
            if hole_grid[row][col] == False:
                grid[row][col] = number
                pprint(grid)
                print(number)
                time.sleep(0.1)


def fill_empty_quad_value(index, hole_grid, number):
    row_range = get_quadrant_row_range(index)
    col_range = get_quadrant_col_range(index)
    fill_hole_in_range(row_range, col_range, hole_grid, number)


def fill_empty_row_value(index, hole_grid, number):
    row_range = tuple(range(index, index + 1))
    col_range = tuple(range(CONTAINER_LENGTH))
    fill_hole_in_range(row_range, col_range, hole_grid, number)


def fill_empty_column_value(index, hole_grid, number):
    row_range = tuple(range(CONTAINER_LENGTH))
    col_range = tuple(range(index, index + 1))
    fill_hole_in_range(row_range, col_range, hole_grid, number)


def fill_holes(slice_and_dice_containers, hole_grid, target_number):
    for container_name, container in slice_and_dice_containers.items():
        for index, container_list in container.items():
            # check if there is a container with only one hole
            if len(container_list) != CONTAINER_LENGTH - 1:
                continue
            if container_name == "quads":
                fill_empty_quad_value(index, hole_grid, target_number)
                continue
            if container_name == "rows":
                fill_empty_row_value(index, hole_grid, target_number)
                continue
            if container_name == "cols":
                fill_empty_column_value(index, hole_grid, target_number)
                continue


def slice_and_dice_all_numbers(containers, numbers=NUMBERS):
    """slice and dice uses the process of elimination to find holes"""
    for target_number in numbers:
        hole_grid = get_slice_and_dice_grid(containers, target_number)
        slice_and_dice_containers = get_new_containers()
        update_containers(slice_and_dice_containers, hole_grid)
        fill_holes(slice_and_dice_containers, hole_grid, target_number)


def get_new_containers():
    quadrants = DefaultDict(list)
    rows = DefaultDict(list)
    columns = DefaultDict(list)
    return {"quads": quadrants, "rows": rows, "cols": columns}


def main():
    containers = get_new_containers()
    last_grid = None
    while last_grid != GRID:
        last_grid = copy.deepcopy(GRID)
        update_containers(containers)
        slice_and_dice_all_numbers(containers)
        pprint(GRID)


if __name__ == "__main__":
    main()

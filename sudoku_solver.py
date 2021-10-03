import math
from typing import DefaultDict
from pprint import pprint
import time
import copy

QUADRANT_LENGTH = 3
CONTAINER_LENGTH = QUADRANT_LENGTH ** 2


NUMBERS = list(range(1, CONTAINER_LENGTH + 1))
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
    container_dict[index].append(value)


def update_slice_and_dice_containers(containers, grid=GRID):
    for row, row_list in enumerate(grid):
        for col, value in enumerate(row_list):
            if value == 0 or value == False:
                continue
            add_to_container(containers["rows"], row, value)
            add_to_container(containers["cols"], col, value)
            quad_index = get_quadrant_index(row, col)
            add_to_container(containers["quads"], quad_index, value)


def update_elimination_containers(elimination_containers, elimination_grid):
    for row, row_list in enumerate(elimination_grid):
        for col, option_list in enumerate(row_list):
            if not isinstance(option_list, list):
                continue
            option_list.sort()
            elimination_containers["rows"][row][(row, col)] = option_list
            elimination_containers["cols"][col][(row, col)] = option_list
            quad_index = get_quadrant_index(row, col)
            elimination_containers["quads"][quad_index][(row, col)] = option_list


def build_false_grid(grid_size=CONTAINER_LENGTH):
    grid = []
    for row in range(grid_size):
        row = []
        for col in range(grid_size):
            row.append(False)
        grid.append(row)
    return grid


def in_container(container_dict, index, value):
    if value in container_dict[index]:
        return True


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
                # pprint(grid)
                # print(number)
                time.sleep(0.1)


def get_quad_range(index):
    row_range = get_quadrant_row_range(index)
    col_range = get_quadrant_col_range(index)
    return row_range, col_range


def get_row_range(index):
    row_range = tuple(range(index, index + 1))
    col_range = tuple(range(CONTAINER_LENGTH))
    return row_range, col_range


def get_column_range(index):
    row_range = tuple(range(CONTAINER_LENGTH))
    col_range = tuple(range(index, index + 1))
    return row_range, col_range


def fill_holes(slice_and_dice_containers, hole_grid, target_number):
    for container_name, container in slice_and_dice_containers.items():
        for index, container_list in container.items():
            # check if there is a container with only one hole
            if len(container_list) != CONTAINER_LENGTH - 1:
                continue
            elif container_name == "quads":
                row_range, col_range = get_quad_range(index)
            elif container_name == "rows":
                row_range, col_range = get_row_range(index)
            elif container_name == "cols":
                row_range, col_range = get_column_range(index)
            else:
                continue
            fill_hole_in_range(row_range, col_range, hole_grid, target_number)


def slice_and_dice_all_numbers(containers, numbers=NUMBERS):
    """slice and dice uses the process of elimination to find holes"""
    for target_number in numbers:
        hole_grid = get_slice_and_dice_grid(containers, target_number)
        slice_and_dice_containers = get_new_containers()
        update_slice_and_dice_containers(slice_and_dice_containers, hole_grid)
        fill_holes(slice_and_dice_containers, hole_grid, target_number)


def get_new_containers():
    quadrants = DefaultDict(list)
    rows = DefaultDict(list)
    columns = DefaultDict(list)
    return {"quads": quadrants, "rows": rows, "cols": columns}


def get_new_elimination_containers():
    quadrants = DefaultDict(dict)
    rows = DefaultDict(dict)
    columns = DefaultDict(dict)
    return {"quads": quadrants, "rows": rows, "cols": columns}


def find_potential_numbers(containers, row, col):
    eliminated_set = set()
    quad_index = get_quadrant_index(row, col)

    eliminated_set = (
        containers["rows"][row]
        + containers["cols"][col]
        + containers["quads"][quad_index]
    )
    eliminated_set = set(eliminated_set)

    potentials = copy.copy(NUMBERS)
    for eliminated_number in eliminated_set:
        potentials.remove(eliminated_number)
    return potentials


def build_elimination_grid(containers, grid=GRID):
    potential_grid = copy.deepcopy(grid)
    for row, row_list in enumerate(grid):
        for col, value in enumerate(row_list):
            if value == 0:
                potentials = find_potential_numbers(containers, row, col)
                if len(potentials) == 1:
                    grid[row][col] = potentials[0]
                    potential_grid[row][col] = potentials[0]
                else:
                    potential_grid[row][col] = potentials
    return potential_grid


def build_elimination_containers(elimination_grid):
    elimination_containers = get_new_elimination_containers()
    update_elimination_containers(elimination_containers, elimination_grid)
    return elimination_containers


def eliminate_options(options_list, elimination_grid):
    option_dict = DefaultDict(int)
    for (row, col), options in options_list:
        option_dict[options] += 1


def option_elimination(elimination_containers, elimination_grid):
    for containers_group in elimination_containers.values():
        for options_list in containers_group.values():
            eliminate_options(options_list, elimination_grid)


def eliminate(containers):
    elimination_grid = build_elimination_grid(containers)
    elimination_containers = build_elimination_containers(elimination_grid)
    option_elimination(elimination_containers, elimination_grid)


def main():
    containers = get_new_containers()
    for _ in range(2):
        last_grid = None
        while last_grid != GRID:
            last_grid = copy.deepcopy(GRID)
            update_slice_and_dice_containers(containers)
            slice_and_dice_all_numbers(containers)
            print("slice and dice round:")
            pprint(GRID)

        last_grid = None
        while last_grid != GRID:
            last_grid = copy.deepcopy(GRID)
            update_slice_and_dice_containers(containers)
            eliminate(containers)
            print("elimination round:")
            pprint(GRID)


if __name__ == "__main__":
    main()

import math
from typing import DefaultDict

GRID = [
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


def get_quadrant_row_start(row, base=3):
    """get the starting number of each row"""
    return base * math.floor(row / base)


def get_quadrant_col(col, base=3):
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


def add_to_dict(dict_ref, index, value):
    if value == 0:
        return
    dict_ref[index].add(value)


def update_containers(containers, grid=GRID):
    for row, row_list in enumerate(grid):
        for col, value in enumerate(row_list):
            add_to_dict(containers["rows"], row, value)
            add_to_dict(containers["cols"], col, value)
            quad_index = get_quadrant_index(row, col)
            print(quad_index)
            add_to_dict(containers["quads"], quad_index, value)


def main():
    quadrants = DefaultDict(set)
    rows = DefaultDict(set)
    columns = DefaultDict(set)

    containers = {"quads": quadrants, "rows": rows, "cols": columns}
    update_containers(containers)
    print(containers)


if __name__ == "__main__":
    main()

#!/usr/bin/python3

# Advent of Code Day 8
# Jakob M. Krieger

# --- imports ---

from itertools import product
from collections import defaultdict

import numpy as np

# ------

def get_adjacents(pos, shape):
    # numpy is [row, col]
    is_outermost_left = pos[1] == 0
    is_outermost_right = pos[1] == shape[1] - 1
    is_outermost_top = pos[0] == 0
    is_outermost_bottom = pos[0] == shape[0] - 1
    adjacent_positions = list()
    if not is_outermost_left:
        adjacent_positions.append((pos[0], pos[1] - 1))
    if not is_outermost_right:
        adjacent_positions.append((pos[0], pos[1] + 1))
    if not is_outermost_top:
        adjacent_positions.append((pos[0] - 1, pos[1]))
    if not is_outermost_bottom:
        adjacent_positions.append((pos[0] + 1, pos[1]))
    return adjacent_positions


def get_minima_mask(height_map, dh=1) -> list[tuple]:
    minima_mask = np.zeros(height_map.shape)
    for pos in product(range(height_map.shape[0]), range(height_map.shape[1])):
        val = height_map[pos]
        adjacent_pos = get_adjacents(pos, height_map.shape)
        adjacent_vals = np.array([height_map[adj_pos] for adj_pos in adjacent_pos])
        minima_mask[pos] = all((val + dh) <= adjacent_vals)
    return minima_mask


def get_risk_level(height_map, minima_mask):
    minima_vals = height_map[np.where(minima_mask)]
    return len(minima_vals) + sum(minima_vals)


# --- part 1 ---

def part1():
    return get_risk_level(PUZZLE_INPUT, get_minima_mask(PUZZLE_INPUT))


# --- part 2 ---

#import plotly.express as px

def get_basin_map(height_map):
    minima_mask = get_minima_mask(height_map)
    minima = np.where(minima_mask)
    # 1) get successively adjacents of all minima
    # 2) check whether at these adjacents the height map is smaller than 9
    # 3) if so, add the position to the basin
    basin_map = np.zeros(height_map.shape, dtype=int)
    for basin_id, minimum_pos in enumerate(zip(minima[0], minima[1]), start=1):
        basin_frontier = set([minimum_pos])
        basin_cells = set()
        basin_is_closed = False
        while not basin_is_closed:
            old_len_basins_cells = len(basin_cells)
            new_frontier_cells = set()
            for frontier_cell in basin_frontier:
                if height_map[frontier_cell] < 9:
                    basin_map[frontier_cell] = basin_id
                    basin_cells |= set(frontier_cell)
                    new_frontier_cells |= set(get_adjacents(frontier_cell, height_map.shape))
            basin_frontier |= new_frontier_cells
            basin_frontier -= basin_cells
            #px.imshow(basin_map).show()
            if len(basin_cells) == old_len_basins_cells:
                basin_is_closed = True
    return basin_map

def get_size_of_basin(basin_map, basin_id):
    return sum(basin_map.flatten() == basin_id)

def part2():
    basin_map = get_basin_map(PUZZLE_INPUT)
    three_largest_basins_sizes = sorted([get_size_of_basin(basin_map, basin_id) for basin_id in range(1, basin_map.max())], reverse=True)[:3]
    return np.prod(three_largest_basins_sizes)


# --- main ---

if __name__ == "__main__":
    with open("input_day09.txt", "r") as f:
        PUZZLE_INPUT_STR = [line.replace("\n", "") for line in f.readlines()]
        PUZZLE_INPUT = np.array([list(map(int, line)) for line in PUZZLE_INPUT_STR])
    risk_level, basin_map_prod = part1(), part2()
    print(risk_level, basin_map_prod)

#!/usr/bin/python3

PUZZLE_INPUT = [1,1,1,1,1,1,1,4,1,2,1,1,4,1,1,1,5,1,1,1,1,1,1,1,1,1,1,1,1,5,1,1,1,1,3,1,1,2,1,2,1,3,3,4,1,4,1,1,3,1,1,5,1,1,1,1,4,1,1,5,1,1,1,4,1,5,1,1,1,3,1,1,5,3,1,1,1,1,1,4,1,1,1,1,1,2,4,1,1,1,1,4,1,2,2,1,1,1,3,1,2,5,1,4,1,1,1,3,1,1,4,1,1,1,1,1,1,1,4,1,1,4,1,1,1,1,1,1,1,2,1,1,5,1,1,1,4,1,1,5,1,1,5,3,3,5,3,1,1,1,4,1,1,1,1,1,1,5,3,1,2,1,1,1,4,1,3,1,5,1,1,2,1,1,1,1,1,5,1,1,1,1,1,2,1,1,1,1,4,3,2,1,2,4,1,3,1,5,1,2,1,4,1,1,1,1,1,3,1,4,1,1,1,1,3,1,3,3,1,4,3,4,1,1,1,1,5,1,3,3,2,5,3,1,1,3,1,3,1,1,1,1,4,1,1,1,1,3,1,5,1,1,1,4,4,1,1,5,5,2,4,5,1,1,1,1,5,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,5,1,1,1,1,1,1,3,1,1,2,1,1]

from tqdm import tqdm

# --- PART ONE ---

def simulate_N(days: int, fish_population: list) -> int:
	_fish_population = fish_population.copy()
	for _ in tqdm(range(days)):
		new_fishes = []
		for i, fish in enumerate(_fish_population):
			if fish == 0:
				new_fishes.append(8)
				_fish_population[i] = 6
			else:
				_fish_population[i] -= 1
		_fish_population.extend(new_fishes)

	return len(_fish_population)

print(simulate_N(80, PUZZLE_INPUT))

# --- PART TWO ---

from collections import Counter

def simulate_N_optimized(days: int, fish_population: list) -> int:
	_fish_population = Counter(fish_population)
	for _ in tqdm(range(days)):
		_new = Counter()
		for age, n_age in _fish_population.items():
			_new[age-1] = n_age
		_new[6] += _new[-1]
		_new[8] += _new[-1]
		_new[-1] = 0
		_fish_population = _new
	return _fish_population.total()

print(simulate_N_optimized(256, PUZZLE_INPUT))
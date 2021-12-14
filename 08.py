#!/usr/bin/python3

# Advent of Code Day 8
# Jakob M. Krieger

from collections import defaultdict

with open("input_day08.txt", "r") as f:
    PUZZLE_INPUT = []
    for line in f.readlines():
        signal_patterns_str, output_value_str = line.split(" | ")
        PUZZLE_INPUT.append({
            "signal_patterns": signal_patterns_str.split(), 
            "output_values": output_value_str.split()
        })

SEVEN_SEGMENT_KEY = {
    0: set("abcefg"), 
    1: set("cf"),
    2: set("acdeg"),
    3: set("acdfg"),
    4: set("bcdf"),
    5: set("abdfg"),
    6: set("abdefg"),
    7: set("acf"),
    8: set("abcdefg"),
    9: set("abcdfg")
}

flipped_seven_segment = dict()
for key, val in SEVEN_SEGMENT_KEY.items():
    flipped_seven_segment.update({
        "".join(sorted("".join(val))): key
    })

# number: unique length of activated segments 
SEVEN_SEGMENT_NUMBERS_OF_UNIQUE_LENGTH = {
    1: 2,
    4: 4,
    7: 3,
    8: 7
}

# --- part 1 ---

def part1():
    n = 0
    for _display in PUZZLE_INPUT:
        n += sum([1 for ov in _display["output_values"] if len(ov) in SEVEN_SEGMENT_NUMBERS_OF_UNIQUE_LENGTH.values()])
    return n

# --- part 2 ---

def find_mapping_by_length(standard_sets: list[set], input_sets: list[set]) -> dict:
    """
    Find a mapping between a standard pattern mapping and input sets with an arbitrary pattern by length.
    The existence of such mapping is not guranteed.

    Args
    ----
    standard_sets: list[set]
        A list containing the standard patterns
    input_sets : list[set]
        The input containing 

    Returns
    -------
    mapping: dict
        The mapping which connects the standard patterns to the pattern mapping in the input

    Notes
    -----
    Algorithm steps:

    1) Find all pairs which exlusive set has a magnitude of one.
    2) Get the mapping of these.
    3) Repeat step one, but existing mapping elements are not counted.
    """
    #exclusionary_sets = {(len(set_i), len(set_j)): set_i ^ set_j for set_i in standard_sets for set_j in standard_sets if len(set_i ^ set_j) == 1}
    input_sets_by_length = defaultdict(list)
    for inp_set in input_sets:
        input_sets_by_length[len(inp_set)].append(set(inp_set))
    #print(f"Input sets by length: {input_sets_by_length}")

    def step(standard_sets: list, mapping: dict):
        for set_i in standard_sets:
            for set_j in standard_sets:
                #print(f"current mapping: {mapping}")
                set_i, set_j = set_i.copy(), set_j.copy()
                excl = set_i - set_j
                #print(f"excl_1: {excl}")
                excl = excl - set(mapping.keys())
                #print(f"excl_2: {excl}")
                if len(excl) == 1:
                    left_side = list(excl)[0]
                    #print(f"left side: {left_side}")
                    potential_right_sides = set()
                    for inp_set_ii in input_sets_by_length[len(set_i)]:
                        for inp_set_jj in input_sets_by_length[len(set_j)]:
                            potential_right_sides |= (inp_set_ii - inp_set_jj - set(mapping.values()))
                    #print(f"potential right sides: {potential_right_sides}")
                    if len(potential_right_sides) == 1:
                        right_side = list(potential_right_sides)[0]
                        #print(f"left side: {left_side}")
                        #print(f"right side: {right_side}")
                        mapping.update({left_side: right_side})
        return mapping

    mapping = dict()
    while len(mapping) <= len(standard_sets):
        new_mapping = step(standard_sets, mapping)
        if mapping == new_mapping:
            return mapping
        else:
            mapping.update(new_mapping)
    
    return mapping

def flip_dict(d: dict):
    return {val: key for key, val in d.items()}


def apply_mapping(mapping: dict, data: list[str], flip_mapping=True, sort=True):
    if flip_mapping:
        mapping = flip_dict(mapping)
    if sort:
        fun = sorted
    else:
        fun = str
    return ["".join(fun("".join([mapping[char] for char in el]))) for el in data] # that's not pretty I know


def part2():
    result = 0
    for _display in PUZZLE_INPUT:
        mapping = find_mapping_by_length(
            SEVEN_SEGMENT_KEY.values(),
            _display["signal_patterns"])

        decoded_vals_str_list = apply_mapping(mapping, _display["output_values"])
        decoded_value = int("".join([str(flipped_seven_segment[dvs]) for dvs in decoded_vals_str_list]))
        result += decoded_value
    
    return result

if __name__ == "__main__":
    print(part1(), part2())

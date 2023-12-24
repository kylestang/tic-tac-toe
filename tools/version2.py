import json

# HELPER FUNCTIONS


def get_tile_value(board: int, tile: int):
    assert 0 <= tile <= 8
    return (board >> (tile * 2)) & 0b11


def rotate_board_90(board: int):
    n = 0
    n |= get_tile_value(board, 6)
    n |= get_tile_value(board, 3) << 2
    n |= get_tile_value(board, 0) << 4
    n |= get_tile_value(board, 7) << 6
    n |= get_tile_value(board, 4) << 8
    n |= get_tile_value(board, 1) << 10
    n |= get_tile_value(board, 8) << 12
    n |= get_tile_value(board, 5) << 14
    n |= get_tile_value(board, 2) << 16
    return n


def flip_horizontally(board: int):
    n = 0
    n |= (board & 0b111111) << 12
    n |= board & (0b111111 << 6)
    n |= (board >> 12) & 0b111111
    return n


def has_o_won(board: int) -> bool:
    o_wins = [
            8322, 33288, 133152,    # vertical
            42, 2688, 172032,       # horizontal
            131586, 8736            # diagonal
            ]

    for win_condition in o_wins:
        if win_condition & board == win_condition:
            return True

    return False


def has_x_won(board: int) -> bool:
    x_wins = [
            4161, 16644, 66576,     # vertical
            21, 1344, 86016,        # horizontal
            65793, 4368             # diagonal
            ]

    for win_condition in x_wins:
        if win_condition & board == win_condition:
            return True

    return False


def count_filled_tiles(board: int) -> int:
    filled = 0
    binary = bin(board)[2:].zfill(18)
    for i in range(0, len(binary), 2):
        if '1' in binary[i:i+2]:
            filled += 1

    assert filled <= 9

    return filled


def contains_draw(board: int) -> bool:
    binary = bin(board)[2:].zfill(18)
    for i in range(0, len(binary), 2):
        if '11' == binary[i:i+2]:
            return True

    return False


# Returns a list from 0..4**9 with each value meaning:
# - 0: Not claimed
# - 1: x
# - 2: o
# - 3: Drawn and full
def get_all_boards():
    all_boards = [i for i in range(4**9)]
    return all_boards


# Takes a transitions dict and a state map, and returns a new transitions
# dict and state map with equivalent states merged
def merge_states(original_transitions: dict, state_map: dict):
    all_to_merged = {}
    keys = []
    values = []
    new_map = {}
    new_transitions = {}

    for board, transitions in original_transitions.items():
        if board in [21, 42, 92506]:
            new_map[board] = board
        elif transitions in values:
            index = values.index(transitions)
            new_map[board] = keys[index]
        else:
            values.append(transitions)
            keys.append(board)
            new_map[board] = board

    for board, transitions in original_transitions.items():
        if board in new_map.values():
            new_list = []
            for b, t in transitions:
                new_list.append((new_map[b], t))

            new_transitions[board] = new_list

    for start, end in state_map.items():
        all_to_merged[start] = new_map[end]

    return new_transitions, all_to_merged


# MAPPING FUNCTIONS

# Returns a dict which maps each board value to the new _pruned_ value
# Removes the following:
# - All boards that x has won become 21
# - All boards that o has won become 42
# - All boards that both x and o have won are removed since they can't exist
# - All boards with a drawn tile are removed (Do I want to do this?)
# - All boards that are drawn and full become 92506
def map_all_to_pruned():
    all_boards = get_all_boards()
    pruned_boards = {}
    for board in all_boards:
        x_won = has_x_won(board)
        o_won = has_o_won(board)
        filled_tiles = count_filled_tiles(board)
        drawn = contains_draw(board)

        if x_won and o_won:
            continue
        elif drawn:
            continue
        elif x_won:
            pruned_boards[board] = 21
        elif o_won:
            pruned_boards[board] = 42
        elif filled_tiles == 9:
            pruned_boards[board] = 92506
        else:
            pruned_boards[board] = board

    return pruned_boards


# Returns a dict which maps _pruned_ boards to their rotation
def map_pruned_rotations():
    pruned_boards = map_all_to_pruned().values()
    rotations = {}
    for board in pruned_boards:
        if board in [21, 42, 92506]:
            rotations[board] = board
        else:
            rotations[board] = rotate_board_90(board)

    return rotations


# Returns a dict that maps _indexed_ boards to their rotation
def map_indexed_rotations():
    pruned = map_pruned_rotations()
    index = map_pruned_to_indexed()

    rotations = {}
    for start, end in pruned.items():
        rotations[index[start]] = index[end]

    return rotations


# Returns a dict which maps _pruned_ boards to their reflection
def map_pruned_reflections():
    pruned_boards = map_all_to_pruned().values()
    reflections = {}
    for board in pruned_boards:
        if board in [21, 42, 92506]:
            reflections[board] = board
        else:
            reflections[board] = flip_horizontally(board)

    return reflections


# Returns a dict that maps _indexed_ boards to their reflection
def map_indexed_reflections():
    pruned = map_pruned_reflections()
    index = map_pruned_to_indexed()

    reflections = {}
    for start, end in pruned.items():
        reflections[index[start]] = index[end]

    return reflections


# Returns a dict which maps _pruned_ boards to whether x can win on that board
def map_pruned_x_win():
    o_wins = [
            8322, 33288, 133152,    # vertical
            42, 2688, 172032,       # horizontal
            131586, 8736            # diagonal
            ]

    pruned_boards = map_all_to_pruned().values()
    can_x_win = {}

    for board in pruned_boards:
        can_win = False
        for win in o_wins:
            if board & win == 0:
                can_win = True

        can_x_win[board] = can_win

    return can_x_win


# Returns a dict that maps the _indexed_ boards to whether x can win on that board
def map_indexed_x_win():
    pruned = map_pruned_x_win()
    index = map_pruned_to_indexed()

    can_x_win = {}

    for board, value in pruned.items():
        can_x_win[index[board]] = value

    return can_x_win


# Returns a dict that maps _pruned_ boards to whether o can win on that board
def map_pruned_o_win():
    x_wins = [
            4161, 16644, 66576,     # vertical
            21, 1344, 86016,        # horizontal
            65793, 4368             # diagonal
            ]

    pruned_boards = map_all_to_pruned().values()
    can_o_win = {}

    for board in pruned_boards:
        can_win = False
        for win in x_wins:
            if board & win == 0:
                can_win = True

        can_o_win[board] = can_win

    return can_o_win


# Returns a dict that maps the _indexed_ boards to whether o can win on that board
def map_indexed_o_win():
    pruned = map_pruned_o_win()
    index = map_pruned_to_indexed()

    can_o_win = {}

    for board, value in pruned.items():
        can_o_win[index[board]] = value

    return can_o_win


# Returns a dict that maps _pruned_ boards to possible _pruned_ board
# states for x, and which tile it was put in
# The dict is {board: [(board, tile)]}
def map_pruned_to_x_transitions():
    pruned_boards = map_all_to_pruned()
    x_transitions = {}

    for board in set(pruned_boards.values()):
        transition = []
        if board not in [21, 42, 92506]:
            for tile in range(0, 9):
                if get_tile_value(board, tile) == 0:
                    new_board = pruned_boards[board | (0b1 << (2 * tile))]
                    transition.append((new_board, tile))

        x_transitions[board] = transition

    return x_transitions


# Returns a transitions dict of _pruned_ states with equivalent states _merged_
# Also returns an updated all_to_merged mapping. Return is (transitions, map)
# The resulting dataset is _merged_
def merge_pruned_x_transitions():
    original_transitions = map_pruned_to_x_transitions()
    current_map = map_all_to_pruned()

    old_dict = {}
    new_dict = original_transitions
    print(f"len: {len(new_dict)}")

    while old_dict != new_dict:
        old_dict = new_dict
        new_dict, current_map = merge_states(new_dict, current_map)
        print(f"len: {len(new_dict)}")

    return new_dict, current_map


# Returns a dict that maps _indexed_ boards to possible _indexed_ board
# states for x, and which tile it was put in
# The dict is {board: [(board, tile)]}
def map_indexed_to_x_transitions():
    pruned = map_pruned_to_x_transitions()
    index = map_pruned_to_indexed()
    x_transitions = {}

    for board, possibilities in pruned.items():
        new_p = [(index[b[0]], b[1]) for b in possibilities]
        new_b = index[board]

        x_transitions[new_b] = new_p

    return x_transitions


# Returns a dict that maps _pruned_ boards to possible _pruned_ board
# states for o, and which tile it was put in
# The dict is {board: [(board, tile)]}
def map_pruned_to_o_transitions():
    pruned_boards = map_all_to_pruned()
    o_transitions = {}

    for board in set(pruned_boards.values()):
        transition = []
        for tile in range(0, 9):
            if get_tile_value(board, tile) == 0:
                new_board = pruned_boards[board | (0b10 << (2 * tile))]
                transition.append((new_board, tile))

        o_transitions[board] = transition

    return o_transitions


# Returns a dict that maps _indexed_ boards to possible _indexed_ board
# states for o, and which tile it was put in
# The dict is {board: [(board, tile)]}
def map_indexed_to_o_transitions():
    pruned = map_pruned_to_o_transitions()
    index = map_pruned_to_indexed()
    o_transitions = {}

    for board, possibilities in pruned.items():
        new_p = [(index[b[0]], b[1]) for b in possibilities]
        new_b = index[board]

        o_transitions[new_b] = new_p

    return o_transitions


# Maps the _pruned_ boards to the _indexed_ boards
def map_pruned_to_indexed():
    pruned_boards = set(map_all_to_pruned().values())
    indexed = {}
    for i, board in enumerate(sorted(list(pruned_boards))):
        indexed[board] = i

    return indexed


# Maps _all_ boards to the _indexed_ boards
def map_all_to_indexed():
    pruned_boards = map_all_to_pruned()
    indexed = {}

    pruned_to_indexed = map_pruned_to_indexed()

    for all_board, pruned_board in pruned_boards.items():
        indexed[all_board] = pruned_to_indexed[pruned_board]

    return indexed


# PRINTING FUNCTIONS

# Prints a mapping from all boards to _pruned_ boards
def print_all_to_pruned():
    boards = map_all_to_pruned()
    output = json.dumps(boards, indent=2)
    with open("all_to_pruned.json", "w") as f:
        f.write(output)


# Prints a mapping from _pruned_ board to rotated _pruned_ board
def print_pruned_rotations():
    boards = map_pruned_rotations()
    output = json.dumps(boards, indent=2)
    with open("pruned_to_rotated.json", "w") as f:
        f.write(output)


# Prints a mapping from _pruned_ boards to reflected _pruned_ boards
def print_pruned_reflections():
    boards = map_pruned_reflections()
    output = json.dumps(boards, indent=2)
    with open("pruned_to_reflected.json", "w") as f:
        f.write(output)


# Prints a mapping from _pruned_ boards to whether x can win on them
def print_pruned_to_x_wins():
    boards = map_pruned_x_win()
    output = json.dumps(boards, indent=2)
    with open("pruned_to_x_wins.json", "w") as f:
        f.write(output)


# Prints a mapping from _pruned_ boards to whether o can win on them
def print_pruned_to_o_wins():
    boards = map_pruned_o_win()
    output = json.dumps(boards, indent=2)
    with open("pruned_to_o_wins.json", "w") as f:
        f.write(output)


# Prints a mapping from _pruned_ boards to whether x can win on them
def print_pruned_to_x_transitions():
    boards = map_pruned_to_x_transitions()
    output = json.dumps(boards, indent=2)
    with open("pruned_to_x_transitions.json", "w") as f:
        f.write(output)


# Prints a mapping from _pruned_ boards to o's possible moves
def print_pruned_to_o_transitions():
    boards = map_pruned_to_o_transitions()
    output = json.dumps(boards, indent=2)
    with open("pruned_to_o_transitions.json", "w") as f:
        f.write(output)


# Prints a mapping from _all_ boards to _merged_ boards, and whether x can
# win on them
def print_merged_x_transitions():
    transitions, boards = merge_pruned_x_transitions()
    output = json.dumps(boards, indent=2)
    with open("all_to_merged.json", "w") as f:
        f.write(output)
    output = json.dumps(transitions, indent=2)
    with open("merged_to_x_transitions.json", "w") as f:
        f.write(output)


# Prints a mapping from _all_ boards to _indexed_ boards
def print_all_to_indexed():
    boards = map_all_to_indexed()
    output = json.dumps(boards, indent=2)
    with open("all_to_indexed.json", "w") as f:
        f.write(output)


# Prints a mapping from _indexed_ boards to rotated boards
def print_indexed_to_rotations():
    boards = map_indexed_rotations()
    output = json.dumps(boards, indent=2)
    with open("indexed_to_rotations.json", "w") as f:
        f.write(output)


# Prints a mapping from _indexed_ boards to reflected boards
def print_indexed_to_reflections():
    boards = map_indexed_reflections()
    output = json.dumps(boards, indent=2)
    with open("indexed_to_reflections.json", "w") as f:
        f.write(output)


# Prints a mapping from _indexed_ boards to whether the board can be won by x
def print_indexed_to_x_win():
    boards = map_indexed_x_win()
    output = json.dumps(boards, indent=2)
    with open("indexed_to_x_win.json", "w") as f:
        f.write(output)


# Prints a mapping from _indexed_ boards to whether the board can be won by o
def print_indexed_to_o_win():
    boards = map_indexed_o_win()
    output = json.dumps(boards, indent=2)
    with open("indexed_to_o_win.json", "w") as f:
        f.write(output)


# Prints a mapping from _indexed_ boards to whether x can win on them
def print_indexed_to_x_transitions():
    boards = map_indexed_to_x_transitions()
    output = json.dumps(boards, indent=2)
    with open("indexed_to_x_transitions.json", "w") as f:
        f.write(output)


# Prints a rust friendly representation of the possible transitions for x
# from each _indexed_ board
def print_rust_x_transitions():
    boards = map_indexed_to_x_transitions()
    boards_enum = [
            "TopLeft",
            "TopCentre",
            "TopRight",
            "CentreLeft",
            "Centre",
            "CentreRight",
            "BottomLeft",
            "BottomCentre",
            "BottomRight"
            ]

    output = f"pub const X_TRANSITIONS: [&[(u32, Boards)]; {len(boards)}] = [\n"
    for board, transitions in boards.items():
        output += "&["
        for t in transitions:
            output += f"({t[0]}, {boards_enum[t[1]]}), "
        output += "],\n"

    output += "];"

    with open("rust_x_transitions.txt", "w") as f:
        f.write(output)


# Prints a mapping from _indexed_ boards to whether o can win on them
def print_indexed_to_o_transitions():
    boards = map_indexed_to_o_transitions()
    output = json.dumps(boards, indent=2)
    with open("indexed_to_o_transitions.json", "w") as f:
        f.write(output)


# Prints a rust friendly representation of the possible transitions for o
# from each _indexed_ board
def print_rust_o_transitions():
    boards = map_indexed_to_o_transitions()
    boards_enum = [
            "TopLeft",
            "TopCentre",
            "TopRight",
            "CentreLeft",
            "Centre",
            "CentreRight",
            "BottomLeft",
            "BottomCentre",
            "BottomRight"
            ]

    output = f"pub const O_TRANSITIONS: [&[(u32, Boards)]; {len(boards)}] = [\n"
    for board, transitions in boards.items():
        output += "&["
        for t in transitions:
            output += f"({t[0]}, {boards_enum[t[1]]}), "
        output += "],\n"

    output += "];"

    with open("rust_o_transitions.txt", "w") as f:
        f.write(output)


print_all_to_pruned()
print_pruned_rotations()
print_pruned_reflections()
print_pruned_to_x_wins()
print_pruned_to_o_wins()
print_pruned_to_x_transitions()
print_pruned_to_o_transitions()
print_all_to_indexed()
print_indexed_to_rotations()
print_indexed_to_reflections()
print_indexed_to_x_win()
print_indexed_to_o_win()
print_indexed_to_x_transitions()
print_indexed_to_o_transitions()
print_rust_x_transitions()
print_rust_o_transitions()
print_merged_x_transitions()

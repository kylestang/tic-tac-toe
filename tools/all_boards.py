# All boards is 0..4**9
import json


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


def is_normalized(board: int, normalized_boards: list[int]) -> bool:
    for _ in range(4):
        if board in normalized_boards:
            return True
        else:
            board = rotate_board_90(board)

    board = flip_horizontally(board)
    for _ in range(4):
        if board in normalized_boards:
            return True
        else:
            board = rotate_board_90(board)

    return False


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


def normalize_boards() -> list:
    normalized_boards = []

    for board in range(0, 4**9):
        if board % 10000 == 0:
            print(board)

        bad = False
        for i in range(9):
            if board & (0b11 << (i * 2)) == 0b11 << (i * 2):
                bad = True
                break

        if bad:
            continue

        found = is_normalized(board, normalized_boards)
        if not found:
            normalized_boards.append(board)

    return normalized_boards


def get_normalization(board: int, all_boards: dict) -> bool:
    for _ in range(4):
        if board in all_boards.values():
            return board
        else:
            board = rotate_board_90(board)

    board = flip_horizontally(board)
    for _ in range(4):
        if board in all_boards.values():
            return board
        else:
            board = rotate_board_90(board)

    return flip_horizontally(board)


def all_to_normalized():
    all = {}
    for board in range(0, 4**9):
        bad = False
        for i in range(9):
            if board & (0b11 << (i * 2)) == 0b11 << (i * 2):
                bad = True
                break

        if bad:
            continue

        n = get_normalization(board, all)
        all[board] = n

    return all


def remove_impossible(boards: list[int]) -> list[int]:
    b = []
    for board in boards:
        if not (has_x_won(board) or has_o_won(board)):
            b.append(board)

    return b


def prune_all_map(all: dict) -> dict:
    new_all = {}
    for board, normalized in all.items():
        x_win = count_x_wins(board)
        o_win = count_o_wins(board)

        if x_win > 0 and o_win > 0:
            continue
        elif x_win > 0:
            new_all[board] = 21
        elif o_win > 0:
            new_all[board] = 42
        else:
            new_all[board] = normalized

    return new_all


def count_o_wins(board: int) -> bool:
    o_wins = [
            8322, 33288, 133152,    # vertical
            42, 2688, 172032,       # horizontal
            131586, 8736            # diagonal
            ]
    w = 0

    for win_condition in o_wins:
        if win_condition & board == win_condition:
            w += 1

    return w


def count_x_wins(board: int) -> bool:
    x_wins = [
            4161, 16644, 66576,     # vertical
            21, 1344, 86016,        # horizontal
            65793, 4368             # diagonal
            ]
    w = 0

    for win_condition in x_wins:
        if win_condition & board == win_condition:
            w += 1

    return w


def find_transitions(all_boards: dict, normalized: list[int]) -> dict:
    transitions = {}
    for board in normalized:
        x_transitions = set()
        o_transitions = set()
        for tile in range(9):
            if get_tile_value(board, tile) == 0:
                x1 = board | (0b1 << (2 * tile))
                x2 = all_boards[x1]
                x_transitions.add(x2)

                o1 = board | (0b10 << (2 * tile))
                o2 = all_boards[o1]
                o_transitions.add(o2)

        x_transitions.discard(board)
        o_transitions.discard(board)
        transitions[board] = {
                'x': list(x_transitions),
                'o': list(o_transitions)
                }

    return transitions


def print_all_to_normalized():
    all = all_to_normalized()
    s = json.dumps(all, indent=2)
    print(len(set(all.values())))
    with open("all_to_normalized.json", "w") as f:
        f.write(s)


def print_all_to_normalized_pruned():
    all = all_to_normalized()
    all = prune_all_map(all)
    print(len(set(all.values())))
    s = json.dumps(all, indent=2)
    with open("all_to_normalized_pruned.json", "w") as f:
        f.write(s)


def print_normalized_transitions():
    all = all_to_normalized()
    all = prune_all_map(all)
    normalized = list(set(all.values()))
    transitions = find_transitions(all, normalized)
    print(len(transitions.keys()))
    s = json.dumps(transitions, indent=2)
    with open("normalized_transitions.json", "w") as f:
        f.write(s)


# print_all_to_normalized()
# print_all_to_normalized_pruned()
print_normalized_transitions()







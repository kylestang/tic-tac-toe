import sys

def calculate_my_wins():
    win_states = [[
            1,1,1,
            0,0,0,
            0,0,0,
        ],[
            0,0,0,
            1,1,1,
            0,0,0,
        ],[
            0,0,0,
            0,0,0,
            1,1,1,
        ],[
            1,0,0,
            1,0,0,
            1,0,0,
        ],[
            0,1,0,
            0,1,0,
            0,1,0,
        ],[
            0,0,1,
            0,0,1,
            0,0,1,
        ],[
            1,0,0,
            0,1,0,
            0,0,1,
        ],[
            0,0,1,
            0,1,0,
            1,0,0,
        ]]


    for state in range(len(win_states)):
        bit_value = 0
        for tile in range(len(win_states[state])):
            bit_value |= win_states[state][tile] << 2 * tile
        
        print(f"Board {state}: {hex(bit_value)}")

def calculate_other_wins():
    win_states = [[
            2,2,2,
            0,0,0,
            0,0,0,
        ],[
            0,0,0,
            2,2,2,
            0,0,0,
        ],[
            0,0,0,
            0,0,0,
            2,2,2,
        ],[
            2,0,0,
            2,0,0,
            2,0,0,
        ],[
            0,2,0,
            0,2,0,
            0,2,0,
        ],[
            0,0,2,
            0,0,2,
            0,0,2,
        ],[
            2,0,0,
            0,2,0,
            0,0,2,
        ],[
            0,0,2,
            0,2,0,
            2,0,0,
        ]]


    for state in range(len(win_states)):
        bit_value = 0
        for tile in range(len(win_states[state])):
            bit_value |= win_states[state][tile] << 2 * tile
        
        print(f"Board {state}: {hex(bit_value)}")

def print_small_board(board: int):
    a = bin(board)[2:].zfill(18)
    print(a)
    out = "-------\n"
    for i in range(3):
        for j in range(3):
            position = 18 - (i * 3 + j) * 2
            tile_value = int(a[position-2:position], 2)
            out += "|" + str(tile_value)
        out += "|\n"
    out += "-------"

    print(out)

def parse_int(num: str) -> int:
    if "x" in num:
        return int(num.split("x")[-1], 16)
    elif "b" in num:
        return int(num.split("b")[-1], 2)
    else:
        return int(num)

if __name__ == "__main__":
    commands = sys.argv
    if commands[1] == "my-wins":
        calculate_my_wins()
    elif commands[1] == "other-wins":
        calculate_other_wins()
    elif commands[1] == "board":
        print_small_board(parse_int(commands[2]))
    else:
        print("Command not found")

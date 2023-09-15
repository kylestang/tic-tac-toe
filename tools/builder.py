
def calculate_win_boards():
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
        
        print(f"Board {state}: {bit_value}")

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

if __name__ == "__main__":
    print_small_board(21)

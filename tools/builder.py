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
            bit_value |= win_states[state][tile] << tile
        
        print(f"Board {state}: {hex(bit_value)}")

def print_small_board(board: int):
    a = bin(board)[2:].zfill(9)
    print(a)
    out = "-------\n"
    for i in range(3):
        for j in range(3):
            position = 9 - (i * 3 + j)
            out += "|" + a[position-1:position]
        out += "|\n"
    out += "-------"

    print(out)

if __name__ == "__main__":
    commands = sys.argv
    if commands[1] == "wins":
        calculate_my_wins()
    elif commands[1] == "board":
        print_small_board(int(commands[2], 0))
    else:
        print("Command not found")

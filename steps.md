# Tasks

1. Enumerate all possible boards
2. Enumerate normalized boards
 - Add special states for x win, y win, impossible. Prune to match
3. Map all boards to normalized boards
4. Map all board + move to all board
5. Map all board + move to normalized board(?)
6. For each normalized board, find list of future possible normalized boards
7. Find list of valid moves for each normalized board
8. Enumerate winning normalized boards

Tile states in base 4:
 - 0: Not claimed
 - 1: x
 - 2: o
 - 3: Drawn

 ## New stuff

 1. Create mapping bewteen each board value and it's rotation

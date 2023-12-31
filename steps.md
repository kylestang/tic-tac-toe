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

3 types of functions: helpers, creators, printers

pruned, merged values: x:21, o: 42, #: 92506
indexed values: x:13, o: 26, #: 5663

Current data flow: all -> pruned -> merged -> indexed

Note: For now I'm pruning all the boards with draw tiles as well, but I can
just modify the prune_all_boards() function if I want them back.
The difference is 11098 without vs 52833 with

### Ideas

- Save all seen states for lookup
- Start by writing minimax
- Prune by looking at whether the big board _can_ be won
  - Later prune further by checking whether small boards can be won to inform big board
- Remember to add alpha/beta pruning
- For transitions, still have list of possible future states, just include the next small board with each move
- Is it better to store all variants of a board in the hashmap or calculate the variants each time?
- How should I order the transitions?
  - Should I put the winning boards first?
  - Should they be ordered or randomized? Ordered could maybe take advantage of the cache but randomized could help avoid biases
- Should I store boards as a u16 rather than a usize? Benchmark
- Add remaining length hints to iterators
- In the p_win and can_p_win functions, should I store the variables first?

### Steps

1. Merge all X wins, O wins, and filled draws into single value
1. Create mapping between each board value and it's rotation
2. Create mapping between each board and it's reflection
4. Create mapping between board value and possible outcomes
5. Merge equivalent states based on possible outcomes, keeping in mind the next move
5. Relabel each _pruned_ board to it's index

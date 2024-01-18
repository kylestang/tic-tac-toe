use ahash::AHashMap;
use tictactoe::state::{Boards, Players, State};
use tictactoe::minimax::minimax;

fn main() {
    // let result = start_minimax();
    let result = test_2();
    println!("{}", result);
}

fn test_2() -> i8 {
    let mut found = AHashMap::new();
    let state = State::new(
        Players::X,
        Boards::Centre,
        5061,
        467,
        13,
        1141,
        6879,
        3381,
        912,
        26,
        2556,
    );

    let result = minimax(state, &mut found);
    result
}

use ahash::AHashMap;
use state::{Players, State};

mod maps;
mod state;

fn main() {
    println!("Hello, world!");
}

fn minimax(state: State, found: &mut AHashMap<State, i32>) -> i32 {
    let known_option = found.get(&state);
    if let Some(&result) = known_option {
        return result;
    }

    if state.turn() == Players::X {
        if state.x_win() {
            for equivalent_state in state.equivalent_states() {
                found.insert(equivalent_state, 1);
            }
            return 1;
        }
    } else {
        if state.o_win() {
            for equivalent_state in state.equivalent_states() {
                found.insert(equivalent_state, -1);
            }
            return -1;
        }
    }
    4
}

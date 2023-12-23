use ahash::AHashMap;
use state::State;

mod constants;
mod state;

fn main() {
    println!("Hello, world!");
}

fn minimax(state: State, found: &mut AHashMap<State, i32>) -> i32 {
    let known_option = state.equivalent_states().find_map(|s| found.get(&s));
    if let Some(&result) = known_option {
        return result;
    }

    if state.x_win() {
        found.insert(state, 1);
        return 1;
    }
    if state.o_win() {
        found.insert(state, -1);
        return -1;
    }
    4
}

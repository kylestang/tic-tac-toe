use ahash::AHashMap;
use state::{Boards, Players, State};

mod maps;
mod state;

fn main() {
    let result = start_minimax();
    println!("{}", result);
}

fn start_minimax() -> i32 {
    let boards = [
        Boards::TopLeft,
        Boards::TopCentre,
        Boards::TopRight,
        Boards::CentreLeft,
        Boards::Centre,
        Boards::CentreRight,
        Boards::BottomLeft,
        Boards::BottomCentre,
        Boards::BottomRight,
    ];
    let mut found = AHashMap::new();
    let mut best = -1;
    for board in boards {
        let state = State::new(Players::X, board, 0, 0, 0, 0, 0, 0, 0, 0, 0);
        let result = minimax(state, &mut found);
        if result > best {
            best = result;
        }
    }
    best
}

fn minimax(state: State, found: &mut AHashMap<State, i32>) -> i32 {
    // Check cache if we've seen this state
    let known_option = found.get(&state);
    if let Some(&result) = known_option {
        return result;
    }

    match state.turn() {
        Players::X => {
            if state.o_win() {
                for equivalent_state in state.equivalent_states() {
                    found.insert(equivalent_state, -1);
                }
                return -1;
            }

            let mut best = -1;
            for future_state in state.future_states() {
                let result = minimax(future_state, found);
                if result == 1 {
                    return 1;
                }
                if result > best {
                    best = result;
                }
            }
            best
        }
        Players::O => {
            if state.x_win() {
                for equivalent_state in state.equivalent_states() {
                    found.insert(equivalent_state, 1);
                }
                return 1;
            }

            let mut best = 1;
            for future_state in state.future_states() {
                let result = minimax(future_state, found);
                if result == -1 {
                    return -1;
                }
                if result < best {
                    best = result;
                }
            }
            best
        }
    }
}

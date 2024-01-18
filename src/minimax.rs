use ahash::AHashMap;
use crate::state::{Boards, Players, State};

fn start_minimax() -> i8 {
    let boards = [
        Boards::TopLeft,
        //        Boards::TopCentre,
        //        Boards::TopRight,
        //        Boards::CentreLeft,
        //        Boards::Centre,
        //        Boards::CentreRight,
        //        Boards::BottomLeft,
        //        Boards::BottomCentre,
        //        Boards::BottomRight,
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

pub fn minimax(state: State, found: &mut AHashMap<State, i8>) -> i8 {
    // Check cache if we've seen this state
    let known_option = state.equivalent_states().find_map(|s| found.get(&s));
    if let Some(&result) = known_option {
        return result;
    }

    let can_x_win = state.can_x_win();
    let can_o_win = state.can_o_win();

    if !can_x_win && !can_o_win {
        return 0;
    }

    match state.turn() {
        Players::X => {
            if state.o_win() {
                return -1;
            }

            let mut best = -1;
            for future_state in state.future_states() {
                let result = minimax(future_state, found);
                if result == 1 {
                    save_state(state, 1, found);
                    return 1;
                } else if result == 0 && !can_x_win {
                    save_state(state, 0, found);
                    return 0;
                }
                if result > best {
                    best = result;
                }
            }
            save_state(state, best, found);
            best
        }
        Players::O => {
            if state.x_win() {
                return 1;
            }

            let mut best = 1;
            for future_state in state.future_states() {
                let result = minimax(future_state, found);
                if result == -1 {
                    save_state(state, -1, found);
                    return -1;
                } else if result == 0 && !can_o_win {
                    save_state(state, 0, found);
                    return 0;
                }
                if result < best {
                    best = result;
                }
            }
            save_state(state, best, found);
            best
        }
    }
}

fn save_state(state: State, value: i8, found: &mut AHashMap<State, i8>) {
    found.insert(state, value);
    println!("Found: {}", found.len() * 8);
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_minimax_1() {
        let mut found = AHashMap::new();
        let state = State::new(
            Players::X,
            Boards::BottomLeft,
            13,
            2949,
            3637,
            26,
            13,
            26,
            13,
            13,
            26,
        );

        let result = minimax(state, &mut found);
        assert_eq!(result, -1);
    }

    #[test]
    fn test_minimax_2() {
        let mut found = AHashMap::new();
        let state = State::new(
            Players::X,
            Boards::TopRight,
            13,
            450,
            1568,
            3638,
            13,
            288,
            4360,
            26,
            154,
        );

        let result = minimax(state, &mut found);
        assert_eq!(result, -1);
    }
}

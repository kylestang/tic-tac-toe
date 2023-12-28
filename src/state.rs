use crate::maps::o_transitions::O_TRANSITIONS;
use crate::maps::reflections::REFLECTIONS;
use crate::maps::rotations::ROTATIONS;
use crate::maps::x_transitions::X_TRANSITIONS;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Players {
    X,
    O,
}

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
pub enum Boards {
    TopLeft,
    TopCentre,
    TopRight,
    CentreLeft,
    Centre,
    CentreRight,
    BottomLeft,
    BottomCentre,
    BottomRight,
}

pub type BoardType = usize;

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
pub struct State {
    turn: Players,
    next_board: Boards,
    top_left: BoardType,
    top_centre: BoardType,
    top_right: BoardType,
    centre_left: BoardType,
    centre: BoardType,
    centre_right: BoardType,
    bottom_left: BoardType,
    bottom_centre: BoardType,
    bottom_right: BoardType,
}

const X_WIN: BoardType = 13;
const O_WIN: BoardType = 26;
const DRAW: BoardType = 5663;

impl State {
    #[inline]
    pub fn turn(self) -> Players {
        self.turn
    }

    #[inline]
    pub fn get_board(self, board: Boards) -> BoardType {
        match board {
            Boards::TopLeft => self.top_left,
            Boards::TopCentre => self.top_centre,
            Boards::TopRight => self.top_right,
            Boards::CentreLeft => self.centre_left,
            Boards::Centre => self.centre,
            Boards::CentreRight => self.centre_right,
            Boards::BottomLeft => self.bottom_left,
            Boards::BottomCentre => self.bottom_centre,
            Boards::BottomRight => self.bottom_right,
        }
    }

    #[inline]
    pub fn set_board(mut self, board: Boards, value: BoardType) -> State {
        match board {
            Boards::TopLeft => self.top_left = value,
            Boards::TopCentre => self.top_centre = value,
            Boards::TopRight => self.top_right = value,
            Boards::CentreLeft => self.centre_left = value,
            Boards::Centre => self.centre = value,
            Boards::CentreRight => self.centre_right = value,
            Boards::BottomLeft => self.bottom_left = value,
            Boards::BottomCentre => self.bottom_centre = value,
            Boards::BottomRight => self.bottom_right = value,
        }

        return self;
    }

    #[inline]
    pub fn x_win(self) -> bool {
        // Horizontal
        (self.top_left == X_WIN && self.top_centre == X_WIN && self.top_right == X_WIN)
            || (self.centre_left == X_WIN && self.centre == X_WIN && self.centre_right == X_WIN)
            || (self.bottom_left == X_WIN && self.bottom_centre == X_WIN && self.bottom_right == X_WIN)
            // Vertical
            || (self.top_left == X_WIN && self.centre_left == X_WIN && self.bottom_left == X_WIN)
            || (self.top_centre == X_WIN && self.centre == X_WIN && self.bottom_centre == X_WIN)
            || (self.top_right == X_WIN && self.centre_right == X_WIN && self.bottom_right == X_WIN)
            // Diagonals
            || (self.top_left == X_WIN && self.centre == X_WIN && self.bottom_right == X_WIN)
            || (self.top_right == X_WIN && self.centre == X_WIN && self.bottom_left == X_WIN)
    }

    #[inline]
    pub fn o_win(self) -> bool {
        // Horizontal
        (self.top_left == O_WIN && self.top_centre == O_WIN && self.top_right == O_WIN)
            || (self.centre_left == O_WIN && self.centre == O_WIN && self.centre_right == O_WIN)
            || (self.bottom_left == O_WIN && self.bottom_centre == O_WIN && self.bottom_right == O_WIN)
            // Vertical
            || (self.top_left == O_WIN && self.centre_left == O_WIN && self.bottom_left == O_WIN)
            || (self.top_centre == O_WIN && self.centre == O_WIN && self.bottom_centre == O_WIN)
            || (self.top_right == O_WIN && self.centre_right == O_WIN && self.bottom_right == O_WIN)
            // Diagonals
            || (self.top_left == O_WIN && self.centre == O_WIN && self.bottom_right == O_WIN)
            || (self.top_right == O_WIN && self.centre == O_WIN && self.bottom_left == O_WIN)
    }

    #[inline]
    fn rotate(self) -> State {
        State {
            turn: self.turn,
            next_board: match self.next_board {
                Boards::TopLeft => Boards::TopRight,
                Boards::TopCentre => Boards::CentreRight,
                Boards::TopRight => Boards::BottomRight,
                Boards::CentreLeft => Boards::TopCentre,
                Boards::Centre => Boards::Centre,
                Boards::CentreRight => Boards::BottomCentre,
                Boards::BottomLeft => Boards::TopLeft,
                Boards::BottomCentre => Boards::CentreLeft,
                Boards::BottomRight => Boards::BottomLeft,
            },
            top_left: ROTATIONS[self.bottom_left],
            top_centre: ROTATIONS[self.centre_left],
            top_right: ROTATIONS[self.top_left],
            centre_left: ROTATIONS[self.bottom_centre],
            centre: ROTATIONS[self.centre],
            centre_right: ROTATIONS[self.top_centre],
            bottom_left: ROTATIONS[self.bottom_right],
            bottom_centre: ROTATIONS[self.centre_right],
            bottom_right: ROTATIONS[self.top_right],
        }
    }

    #[inline]
    fn flip(self) -> State {
        State {
            turn: self.turn,
            next_board: match self.next_board {
                Boards::TopLeft => Boards::BottomLeft,
                Boards::TopCentre => Boards::BottomCentre,
                Boards::TopRight => Boards::BottomRight,
                Boards::CentreLeft => Boards::CentreLeft,
                Boards::Centre => Boards::Centre,
                Boards::CentreRight => Boards::CentreRight,
                Boards::BottomLeft => Boards::TopLeft,
                Boards::BottomCentre => Boards::TopCentre,
                Boards::BottomRight => Boards::TopRight,
            },
            top_left: REFLECTIONS[self.bottom_left],
            top_centre: REFLECTIONS[self.bottom_centre],
            top_right: REFLECTIONS[self.bottom_right],
            centre_left: REFLECTIONS[self.centre_left],
            centre: REFLECTIONS[self.centre],
            centre_right: REFLECTIONS[self.centre_right],
            bottom_left: REFLECTIONS[self.top_left],
            bottom_centre: REFLECTIONS[self.top_centre],
            bottom_right: REFLECTIONS[self.top_right],
        }
    }

    pub fn equivalent_states(self) -> EquivalentStateIter {
        EquivalentStateIter {
            current: self,
            position: 0,
        }
    }

    pub fn future_states(self) -> FutureStateIter {
        let current_value = self.get_board(self.next_board);

        // Check if we can go to all boards
        let all = current_value == X_WIN || current_value == O_WIN || current_value == DRAW;

        FutureStateIter {
            current_state: self,
            position: 0,
            board: self.next_board,
            all,
        }
    }
}

pub struct EquivalentStateIter {
    current: State,
    position: u8,
}

impl Iterator for EquivalentStateIter {
    type Item = State;

    fn next(&mut self) -> Option<Self::Item> {
        if self.position >= 8 {
            return None;
        } else if self.position == 4 {
            self.current = self.current.flip();
        } else if self.position != 0 {
            self.current = self.current.rotate();
        }

        self.position += 1;
        Some(self.current)
    }
}

pub struct FutureStateIter {
    current_state: State,
    position: usize,
    board: Boards,
    all: bool,
}

impl Iterator for FutureStateIter {
    type Item = State;

    fn next(&mut self) -> Option<Self::Item> {
        if self.all {}

        let board_value = self.current_state.get_board(self.current_state.next_board);

        let possibilities = match self.current_state.turn {
            Players::X => X_TRANSITIONS[board_value],
            Players::O => O_TRANSITIONS[board_value],
        };

        if self.position >= possibilities.len() {
            return None;
        }

        let (next_value, next_board) = possibilities[self.position];

        let mut next_state = self.current_state.clone();
        next_state.turn = match next_state.turn {
            Players::X => Players::O,
            Players::O => Players::X,
        };
        next_state = next_state.set_board(self.current_state.next_board, next_value);
        next_state.next_board = next_board;

        self.position += 1;
        Some(next_state)
    }
}

use crate::maps::rotations::ROTATIONS;
use crate::maps::reflections::REFLECTIONS;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
enum Players {
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
    All,
}

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
pub struct State {
    turn: Players,
    next_board: Boards,
    top_left: usize,
    top_centre: usize,
    top_right: usize,
    centre_left: usize,
    centre: usize,
    centre_right: usize,
    bottom_left: usize,
    bottom_centre: usize,
    bottom_right: usize,
}

const X_WIN: usize = 13;
const O_WIN: usize = 26;
const DRAW: usize = 5663;

impl State {
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
                Boards::All => Boards::All,
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
                Boards::All => Boards::All,
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
        } else if self.position == 0 {
            return Some(self.current);
        } else if self.position == 4 {
            self.current = self.current.flip();
        } else {
            self.current = self.current.rotate();
        }

        self.position += 1;
        Some(self.current)
    }
}

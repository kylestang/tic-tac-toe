// Each subboard uses 9 bits, built from https://bitboard.kjs.dev
// So bits 0-80 (inclusive) are subboards
// Bits 81+i are booleans for whether subboard i was won by that player, where 0<=i<=8
// Subboards are numbered 0-8, left to right, then top to bottom
#[derive(Clone, Copy)]
struct Board {
    x: u128,
    o: u128
}

impl Board {
    fn is_won(self, subboard: usize) -> bool {
        let winning_boards = [0x7, 0x38, 0x1c0, 0x49, 0x92, 0x124, 0x111, 0x54];
        true
    }
}

const SUBBOARD_MASK: u128 = 0x1c0e07;


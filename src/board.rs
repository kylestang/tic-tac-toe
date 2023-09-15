// 81x81 tile board, each with 3 states. 2 bits for each tile = 162 bits.
// 192 bits to use smallest number of 64-bit words.
// First 6 boards are first int, 108 bits
// Last 3 boards are 2nd int, 54 bits
// Empty: 0, Mine: 1, Opponent's: 2
#[derive(Clone, Copy)]
struct Board([u32; 9]);
const MY_WIN_STATES: [u32; 8] = [
    0x15, 0x540, 0x15000, 0x1041, 0x4104, 0x10410, 0x10101, 0x1110,
];
const OTHER_WIN_STATES: [u32; 8] = [
    0x2a, 0xa80, 0x2a000, 0x2082, 0x8208, 0x20820, 0x20202, 0x2220,
];

impl Board {
    #[inline]
    fn i_win(&self, board_num: usize) -> bool {
        MY_WIN_STATES
            .iter()
            .any(|&state| state & self.0[board_num] == state)
    }

    #[inline]
    fn other_win(&self, board_num: usize) -> bool {
        OTHER_WIN_STATES
            .iter()
            .any(|&state| state & self.0[board_num] == state)
    }
}

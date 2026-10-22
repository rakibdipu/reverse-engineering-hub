#!/usr/bin/env python3
"""
LeanKeyboard Navigation Engine — Inspired by yuliskov/LeanKeyboard
Simulates a TV-remote optimized 2D matrix on-screen keyboard.
"""

class LeanKeyboardGrid:
    DEFAULT_LAYOUT = [
        ['A', 'B', 'C', 'D', 'E', '1', '2', '3'],
        ['F', 'G', 'H', 'I', 'J', '4', '5', '6'],
        ['K', 'L', 'M', 'N', 'O', '7', '8', '9'],
        ['P', 'Q', 'R', 'S', 'T', '0', '-', '@'],
        ['U', 'V', 'W', 'X', 'Y', 'Z', ' ', '⌫']
    ]

    def __init__(self):
        self.grid = self.DEFAULT_LAYOUT
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.cursor_x = 0
        self.cursor_y = 0

    def move(self, direction: str):
        if direction.upper() == 'UP':
            self.cursor_y = (self.cursor_y - 1) % self.rows
        elif direction.upper() == 'DOWN':
            self.cursor_y = (self.cursor_y + 1) % self.rows
        elif direction.upper() == 'LEFT':
            self.cursor_x = (self.cursor_x - 1) % self.cols
        elif direction.upper() == 'RIGHT':
            self.cursor_x = (self.cursor_x + 1) % self.cols

    def current_char(self):
        return self.grid[self.cursor_y][self.cursor_x]

    def render(self):
        lines = []
        for r, row in enumerate(self.grid):
            line_cells = []
            for c, char in enumerate(row):
                if r == self.cursor_y and c == self.cursor_x:
                    line_cells.append(f"[{char}]")
                else:
                    line_cells.append(f" {char} ")
            lines.append(" ".join(line_cells))
        return "\n".join(lines)

if __name__ == "__main__":
    kb = LeanKeyboardGrid()
    print("Initial LeanKeyboard Grid:")
    print(kb.render())
    print("\nSimulating D-Pad input: RIGHT, RIGHT, DOWN, SELECT")
    kb.move('RIGHT')
    kb.move('RIGHT')
    kb.move('DOWN')
    print(f"Selected Key: '{kb.current_char()}'")

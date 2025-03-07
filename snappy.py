import curses

class NanoClone:
    def __init__(self, stdscr, filename="output.txt"):
        self.stdscr = stdscr
        self.filename = filename
        self.cursor_x = 0
        self.cursor_y = 0
        self.buffer = [""]
        self.load_file()
        self.run_editor()

    def draw_screen(self):
        self.stdscr.clear()
        for i, line in enumerate(self.buffer):
            self.stdscr.addstr(i, 0, line)
        self.stdscr.addstr(curses.LINES - 1, 0, f"CTRL+O to save | CTRL+X to exit | Editing: {self.filename}")
        self.stdscr.move(self.cursor_y, self.cursor_x)
        self.stdscr.refresh()

    def run_editor(self):
        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()

        while True:
            self.draw_screen()
            key = self.stdscr.getch()

            if key == 24:  # CTRL+X to exit
                break
            elif key == 15:  # CTRL+O to save
                self.save_file()
            elif key in (curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN):
                self.move_cursor(key)
            elif key == 10:  # Enter key
                self.buffer.insert(self.cursor_y + 1, "")
                self.cursor_y += 1
                self.cursor_x = 0
            elif key in (127, curses.KEY_BACKSPACE):  # Backspace
                self.handle_backspace()
            elif 32 <= key <= 126:  # Printable characters
                self.buffer[self.cursor_y] = self.buffer[self.cursor_y][:self.cursor_x] + chr(key) + self.buffer[self.cursor_y][self.cursor_x:]
                self.cursor_x += 1

    def move_cursor(self, key):
        if key == curses.KEY_LEFT and self.cursor_x > 0:
            self.cursor_x -= 1
        elif key == curses.KEY_RIGHT and self.cursor_x < len(self.buffer[self.cursor_y]):
            self.cursor_x += 1
        elif key == curses.KEY_UP and self.cursor_y > 0:
            self.cursor_y -= 1
            self.cursor_x = min(self.cursor_x, len(self.buffer[self.cursor_y]))
        elif key == curses.KEY_DOWN and self.cursor_y < len(self.buffer) - 1:
            self.cursor_y += 1
            self.cursor_x = min(self.cursor_x, len(self.buffer[self.cursor_y]))

    def handle_backspace(self):
        if self.cursor_x > 0:
            self.buffer[self.cursor_y] = self.buffer[self.cursor_y][:self.cursor_x - 1] + self.buffer[self.cursor_y][self.cursor_x:]
            self.cursor_x -= 1
        elif self.cursor_y > 0:
            prev_line = self.buffer[self.cursor_y - 1]
            self.cursor_x = len(prev_line)
            self.buffer[self.cursor_y - 1] += self.buffer[self.cursor_y]
            del self.buffer[self.cursor_y]
            self.cursor_y -= 1

    def save_file(self):
        with open(self.filename, "w") as f:
            f.write("\n".join(self.buffer))
        self.stdscr.addstr(curses.LINES - 1, 0, f"Saved to {self.filename}")

    def load_file(self):
        try:
            with open(self.filename, "r") as f:
                self.buffer = f.read().splitlines()
        except FileNotFoundError:
            self.buffer = [""]

if __name__ == "__main__":
    import sys
    filename = sys.argv[1] if len(sys.argv) > 1 else "output.txt"
    curses.wrapper(NanoClone, filename)


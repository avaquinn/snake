import curses
import time
screen = curses.initscr()
screen.clear()

screen.nodelay(True)  # non-blocking keyboard input

while True:
    keyboard_input = screen.getch()
    print keyboard_input
    time.sleep(0.1)

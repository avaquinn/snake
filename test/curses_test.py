import curses

screen = curses.initscr()

screen.addstr(4, 4, "X")
screen.addstr(5, 4, "Y")
screen.addstr(4, 6, "O")


screen.refresh()

curses.napms(50000)
curses.endwin()

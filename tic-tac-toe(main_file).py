import curses
from curses import wrapper
from random import randint


KEY_UP = "w"
KEY_DOWN = "s"
KEY_LEFT = "a"
KEY_RIGHT = "d"
KEY_ENTER = 10
CONTROL_KEYS = list(map(ord, [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]))

def print_matrix(matrix, window, color):
    line_number = 0
    for line in matrix:
        outline = " ".join(line)
        window.addstr(line_number, 0, outline, color)
        line_number += 1
    window.move(0, 0)
    window.refresh()


def check_win_loose(matrix):
    for line in matrix:
        if len(set(line)) == 1 and set(line) != {"-"}:
            return line[0]
    if set([matrix[0][0], matrix[1][1], matrix[2][2]]) in [{"X"}, {"O"}]:
        return matrix[0][0]
    elif set([matrix[0][2], matrix[1][1], matrix[2][0]]) in [{"X"}, {"O"}]:
        return matrix[0][2]
    for col in range(3):
        if set([matrix[0][col], matrix[1][col], matrix[2][col]]) in [{"X"}, {"O"}]:
            return matrix[0][col]


def move_cursor(char_code, playground, color, reverse_color, y, x, matrix):
    if char_code == ord(KEY_UP):
        if coord_is_correct(y-1, x):
            y -= 1
            print_matrix(matrix, playground, reverse_color)
            playground.addstr(y, x, matrix[y][x//2], color)
            playground.move(y, x)
    elif char_code == ord(KEY_DOWN):
        if coord_is_correct(y+1, x):
            y += 1
            print_matrix(matrix, playground, reverse_color)
            playground.addstr(y, x, matrix[y][x//2], color)
            playground.move(y, x)
    elif char_code == ord(KEY_LEFT):
        if coord_is_correct(y, x-2):
            x -= 2
            print_matrix(matrix, playground, reverse_color)
            playground.addstr(y, x, matrix[y][x//2], color)
            playground.move(y, x)
    elif char_code == ord(KEY_RIGHT):
        if coord_is_correct(y, x+2):
            x += 2
            print_matrix(matrix, playground, reverse_color)
            playground.addstr(y, x, matrix[y][x//2], color)
            playground.move(y, x)
    playground.refresh()
    return y, x


def coord_is_correct(y, x):
    return 0 <= y <= 2 and 0 <= x <= 4


@wrapper
def main(stdscr):
    # Set some needed colors----------------------------------------------------
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_MAGENTA)
    white_red = curses.color_pair(1)
    default_color = curses.color_pair(2)
    cursor_color = curses.color_pair(3)
    win_color = curses.color_pair(4)
    reverse = curses.A_REVERSE
    # Output welcome message.
    stdscr.clear()
    lines, cols = curses.LINES - 1, curses.COLS - 1
    welcome_message = "Hello in TIC-TAC-TOE!!!"
    stdscr.addstr(lines // 4, cols // 2 - len(welcome_message) // 2,
                    welcome_message)
    stdscr.addstr(lines // 4 + 1, cols // 2 - len(welcome_message) // 2 - 3,
                    "Press any key to continue...")
    stdscr.refresh()
    stdscr.getch()
    # --------------------------------------------------------------------------
    # Output window to choose "X" or "O"
    choose_window = curses.newwin(2, 20, lines//2 - 2, cols//2 - 7)
    x_choose = "X(First move)"
    o_choose = "O(..........)"
    user_choose, ai_choose = "X", "O"
    x_color, o_color = white_red, default_color
    choose_window.addstr(0, 0, x_choose, x_color)
    choose_window.addstr(1, 0, o_choose, o_color)
    choose_window.move(0, 0)
    choose_window.refresh()
    while True:
        char_code = stdscr.getch()
        stdscr.addstr(0, 0, str(char_code))
        char = chr(char_code).lower()
        if char in [KEY_UP, KEY_DOWN]:
            x_color, o_color = o_color, x_color
            user_choose, ai_choose = ai_choose, user_choose
            choose_window.addstr(0, 0, x_choose, x_color)
            choose_window.addstr(1, 0, o_choose, o_color)
            choose_window.move(0, 0)
            choose_window.refresh()
        elif char_code == KEY_ENTER:
            break
    # clear window after we choose "X" or "O"-----------------------------------
    choose_window.clear()
    choose_window.refresh()
    # --------------------------------------------------------------------------
    user_ai_chars = {
                        user_choose: "USER",
                        ai_choose: "AI",
                    }
    stdscr.addstr(0, 0, str(user_ai_chars))
    stdscr.refresh()
    # --------------------------------------------------------------------------

    # make 'empty' matrix and print playground----------------------------------
    matrix = [["-" for i in range(3)] for j in range(3)]
    playground = curses.newwin(4, 5, lines//2 - 2, cols//2 - 2)
    print_matrix(matrix, playground, reverse)
    # --------------------------------------------------------------------------
    # Main game-loop -----------------------------------------------------------
    y, x = 0, 0
    playground.move(y, x)
    playground.refresh()
    current_move, next_move = "X", "O"
    result = None
    while True:
        # USER-MOVE ------------------------------------------------------------
        if user_ai_chars[current_move] == "USER":
            char_code = stdscr.getch()
            if char_code in CONTROL_KEYS:
                y, x = move_cursor(char_code, playground,
                                    cursor_color, reverse, y, x, matrix)
            elif char_code == KEY_ENTER:
                if matrix[y][x//2] == "-":
                    matrix[y][x//2] = current_move
                    current_move, next_move = next_move, current_move
                    print_matrix(matrix, playground, reverse)
                    playground.move(y, x)
                    result = check_win_loose(matrix)
                    if result in ["X", "O"]:
                        break
        # ----------------------------------------------------------------------
        # AI-MOVE --------------------------------------------------------------
        elif user_ai_chars[current_move] == "AI":

            y, x = randint(0, 2), randint(0, 2)*2
            while matrix[y][x//2] != "-":
                y, x = randint(0, 2), randint(0, 2)*2

            matrix[y][x//2] = current_move
            current_move, next_move = next_move, current_move
            print_matrix(matrix, playground, reverse)
            playground.move(y, x)
            result = check_win_loose(matrix)
            if result in ["X", "O"]:
                break
        # ----------------------------------------------------------------------
        playground.refresh()
    # END WHILE-LOOP -----------------------------------------------------------
    stdscr.addstr(lines - 2, cols//2 - 5, f"Winner: {user_ai_chars[result]}",
                                            win_color)
    stdscr.refresh()
    stdscr.getch()

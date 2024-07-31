""" Handling user input and output """
import curses
import time
from datetime import date
from curses import wrapper
from curses.textpad import Textbox, rectangle
from time import sleep
import os

class CurseWindow:
    def __init__(self, height=15, width=100, begin_y=4, begin_x=2):
        """
        Curse window
        --
        :param height: height of the curse window
        :param width: width of the curse window
        :param begin_y: margin from top
        :param begin_x: margin from left
        --
        Doc: https://docs.python.org/3/howto/curses.html
        """
        self._height = height
        self._width = width
        self._begin_y = begin_y
        self._begin_x = begin_x
        self._win_texteditor = None
        self._win_counter = None

    def input(self, stdscr) -> dict:
        # variables
        MAX_LINES = curses.LINES - 1
        MAX_COLS = curses.COLS - 1
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        GREEN = curses.color_pair(2)
        RED = curses.color_pair(3)

        # init windows
        stdscr.clear()
        self._win_texteditor = curses.newwin(
            self._height,
            self._width,
            self._begin_y,
            self._begin_x
        )
        self._win_counter = curses.newwin(
            1,
            20,
            1,
            2
        )
        win_msg = curses.newwin(
            3,
            30,
            1,
            25
        )

        # counters
        target_words = 20
        words_count = 0
        escape_counter = 3

        text = ""

        self._win_counter.clear()
        self._win_counter.addstr(f'{words_count:03}/{target_words:03} words')
        self._win_counter.refresh()

        while True:
            key = self.get()

            win_msg.clear()
            if chr(key) == ' ':
                words_count += 1
            if key == 27:
                escape_counter -= 1
                if words_count >= target_words or escape_counter == 0:
                    break
                else:
                    win_msg.addstr(0, 0, f'{target_words - words_count} more words to write', RED)
                    win_msg.addstr(1, 0, f'Press ESC {escape_counter} times to surrender', curses.A_DIM)
            else:
                escape_counter = 3
            if words_count > target_words:
                win_msg.addstr(0, 0, f'Target words reached!\nExit by pressing ESC', GREEN)

            self.print(key)
            if key != 127: # delete command
                text += chr(key)

            if chr(key).isspace():
                words_count += 1
            self._win_counter.clear()
            self._win_counter.bkgd(' ')
            self._win_counter.addstr(f'{words_count:03}/{target_words:03} words')

            self._win_counter.refresh()
            win_msg.refresh()
            self._win_texteditor.refresh()

        # saving animation
        Animation.load(self._win_texteditor)

        return {"content": text, "word_count": words_count, "date": str(date.today())}

    @staticmethod
    def option_menu(stdscr):
        stdscr.clear()
        curses.curs_set(0)

        # curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
        # GRAY = curses.color_pair(1)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        GREEN = curses.color_pair(2)

        position = 0
        options = {
            0: "note",
            1: "chat"
        }

        stdscr.addstr(1, 2, "NOTE", GREEN)
        stdscr.addstr(1, 8, "CHAT")
        stdscr.refresh()

        while True:
            rectangle(stdscr, 0, 0, 2, 14)

            ascii = stdscr.getch()
            match ascii:
                case 261:  # RIGHT
                    position = (position + 1) % 2
                case 260:  # LEFT
                    position = abs((position - 1) % 2)
                case 10:  # ENTER
                    break
            if position == 0:
                stdscr.addstr(1, 2, "NOTE", GREEN)
                stdscr.addstr(1, 8, "CHAT")
            else:
                stdscr.addstr(1, 2, "NOTE")
                stdscr.addstr(1, 8, "CHAT", GREEN)

            stdscr.refresh()


        curses.curs_set(1)
        stdscr.clear()
        return options[position]

    def clear(self) -> None:
        self._win_texteditor.clear()

    def refresh(self) -> None:
        self._win_texteditor.refresh()

    def print(self, text: str | int) -> None:
        if isinstance(text, int) and (text == 127 or text == 27):
            return
        if isinstance(text, int):
            text = chr(text)
        self._win_texteditor.addstr(text)
        self._win_texteditor.refresh()

    def get(self) -> int:
        ascii_character = self._win_texteditor.getch()
        return ascii_character

    def getkey(self) -> chr:
        ascii_character = self._win_texteditor.getch()
        return chr(ascii_character)

    def get_and_print(self) -> None:
        character: chr = self.get()
        self.print(character)

    def __str__(self):
        return f"""
        width: {self._width} | height: {self._height}
        area: {self._width * self._height}
        margin: {self._begin_y}(top), {self._begin_x}(left)
        """

    def __del__(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

class TextEditor(CurseWindow):
    """
    Type text one letter at a time and display it on screen
    one after the other
    """
    def __init__(self, stdscr, height=15, width=100, begin_y=3, begin_x=2):
        super().__init__(stdscr, height, width, begin_y, begin_x)
        # self.__box = Textbox(self._window)
        # rectangle(stdscr, 1, 1, height - 1, width - 1)

    # def edit(self) -> None:
    #     self.__box.edit()
    #
    # def gather(self) -> str:
    #     return self.__box.gather().strip()

# class CustomTextbox(Textbox):
#     def __init__(self, win):
#         super().__init__(win)
#         self.char_count = 0
#
#     def do_command(self, ch):
#         # Handle backspace (ASCII 8 or 127)
#         if ch in (curses.KEY_BACKSPACE, 127):
#             if self.char_count > 0:
#                 self.char_count -= 1
#         # Handle printable characters including space
#         elif 32 <= ch <= 126:
#             self.char_count += 1
#         # Let Textbox handle the character
#         super().do_command(ch)
#         # Refresh the window to display updated content
#         self.win.refresh()


class WordCounter(CurseWindow):
    """
    Show word counter header and increment when I type
    """
    def __init__(self, stdscr, target: int, height=1, width=20, begin_y=1, begin_x=2):
        super().__init__(stdscr, height=1, width=40, begin_y=1, begin_x=2)
        self._word_count = 0
        self._char_count = 0
        self._target_word_count = target

    def display(self):
        self.clear()
        self.print(f'{self._word_count}/{self._target_word_count} words')

    def __iadd__(self, other: int):
        self._word_count += other
        return self

    def __isub__(self, other: int):
        self._word_count -= other
        return self

    def __gt__(self, other):
        return self._word_count > other

    def __lt__(self, other):
        return self._word_count < other

    def __eq__(self, other):
        return self._word_count == other

    def __ge__(self, other):
        return self._word_count >= other

    def __le__(self, other):
        return self._word_count <= other

    def __str__(self):
        return f"""
        Word count: {self._word_count} / Target: {self._target_word_count}
        """


def prompt(message: str) -> str:
    """
    Taking user input
    --
    :param message: prompt message
    :return: str, valid user input
    """
    # os.system('cls' if os.name == 'nt' else 'clear')
    print("What would you like to know?")
    ans = ""
    count = 2
    while not ans:
        if count == 0:
            return "#soft-exit#"
        ans = input(f"{message} ")
        count -= 1
    return ans


def stream(message: str, chunk_size=3, delay=0.1) -> None:
    """
    Printing the message 3 characters at a time
    --
    :param message : text message to print be printed
    :param chunk_size : size of each chunk
    :param delay (float)
    :return: None
    """
    n = len(message)
    for i in range(0, n, chunk_size):
        print(message[i:i+chunk_size], end="", flush=True)
        sleep(delay)
    print("")


class Animation:
    """ Animations for the text editor """
    @staticmethod
    def load(screen, rounds=2, before='', after=''):
        curses.curs_set(0)
        yx = screen.getyx()
        frames = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
        n = len(frames)
        for i in range(n * 2):
            screen.addstr(yx[0] + 1, 0, f'\r{frames[i % n]} saving')
            screen.refresh()
            time.sleep(0.1)


# def test(stdscr):
#     w = curses.newwin(3, 18, 2, 2)
#     box = CustomTextbox(w)
#     rectangle(stdscr, 1, 1, 5, 20)
#     text = ""
#
#     while box.char_count < 20:
#         stdscr.refresh()
#         box.edit()
#         res = box.gather()
#         text += res
#         stdscr.addstr(10, 20, f"{text}")
#
#     stdscr.getch()
#     stream(text)
#
# wrapper(test)

if __name__ == "__main__":
    # record()
    pass


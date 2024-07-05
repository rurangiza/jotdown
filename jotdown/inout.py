""" Handling user input and output """
import curses
import time
from curses import wrapper
from curses.textpad import Textbox, rectangle
from time import sleep


class CurseWindow:
    def __init__(self, height, width, begin_y, begin_x):
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
        self._window = curses.newwin(
            self._height,
            self._width,
            self._begin_y,
            self._begin_x
        )
        # MAX_LINES = curses.LINES - 1
        # MAX_COLS = curses.COLS - 1

    def clear(self) -> None:
        self._window.clear()

    def refresh(self) -> None:
        self._window.refresh()

    def print(self, text: str | int) -> None:
        if isinstance(text, int):
            text = chr(text)
        self._window.addstr(text)
        self._window.refresh()

    def get(self) -> chr:
        ascii_character = self._window.getch()
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


class TextArea(CurseWindow):
    """
    Type text one letter at a time and display it on screen
    one after the other
    """
    def __init__(self, height=15, width=100, begin_y=3, begin_x=2):
        super().__init__(height, width, begin_y, begin_x)
        self.__box = Textbox(self._window)
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
    def __init__(self, target: int, height=1, width=20, begin_y=1, begin_x=2):
        super().__init__(height=1, width=40, begin_y=1, begin_x=2)
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


class ChatWindow(CurseWindow):
    """
    Chat app display:
    - ability to type text (left-aligned)
    - get text from LLM (right-aligned)
    """
    def __init__(self):
        pass


def prompt(message: str) -> str:
    """
    Taking user input
    --
    :param message: prompt message
    :return: str, valid user input
    """
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


def loader():
    animation = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
    idx = 0
    while True:
        print(animation[idx % len(animation)], end="\r")
        idx += 1
        sleep(0.1)


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


""" Handling user input and output """
import curses
import time
from curses import wrapper
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
    def __init__(self):
        super().__init__(15, 100, 3, 2)


class WordCounter(CurseWindow):
    """
    Show word counter header and increment when I type
    """
    def __init__(self, target: int):
        super().__init__(1, 20, 1, 2)
        self._word_count = 0
        self._target_word_count = target

    def display(self):
        self.clear()
        self.print(f'{self._word_count}/{self._target_word_count} words')
        self.refresh()

    def __iadd__(self, other: int):
        self._word_count += other
        return self

    def __isub__(self, other: int):
        self._word_count -= other
        return self

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


def record(stdscr):
    # scribe.record()
    stdscr.clear()

    target = 40
    hud = WordCounter(target)
    area = TextArea()

    while target > 0:
        hud.clear()
        hud.display()
        hud.refresh()

        character = area.get()
        area.print(character)
        area.refresh()

        if character.isspace():
            hud += 1
            target -= 1


if __name__ == "__main__":
    wrapper(record)

""" Handling user input and output """
import curses

from curses.textpad import rectangle
from time import sleep

from prompt_toolkit import prompt as input
from prompt_toolkit import print_formatted_text as print

from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.cursor_shapes import CursorShape

from abc import ABC, abstractmethod

from typing import List


class IUserInput(ABC):
    """ Base for all UIs """
    def __init__(self) -> None:
        pass

    @abstractmethod
    def input(self) -> str:
        pass


class CLI(IUserInput):

    def __init__(self) -> None:
        super().__init__()

    def input(self, msg: str = '>>', placeholder: str = 'Type here') -> str:
        """
        Taking user input
        --
        :param msg: prompt message
        :param placeholder: placeholder text after prompt
        :return: str, valid user input
        """
        custom_style = Style.from_dict({
            '': '#ffffff bold',
            'discrete': 'fg:#888888 italic'
        })
        user_input = ""
        count = 2
        print()
        while not user_input:
            if count == 0:
                return "exit!"
            user_input = input(
                HTML(f"{msg} "),
                placeholder=HTML(f'<discrete>{placeholder}</discrete>'),
                cursor=CursorShape.BLINKING_UNDERLINE,
                style=custom_style
            )
            count -= 1
        return user_input


    def stream(self, msg: str, chunk_size = 3, delay = 0.1) -> None:
        """
        Printing the message 3 characters at a time
        --
        :param msg : text message to print be printed
        :param chunk_size : size of each chunk
        :param delay (float)
        :return: None
        """
        n = len(msg)
        for i in range(0, n, chunk_size):
            print(msg[i:i+chunk_size], end="", flush=True)
            sleep(delay)
        print("")


class Editor(IUserInput):
    def __init__(self, height = 15, width = 100, begin_y = 4, begin_x = 2) -> None:
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
        super().__init__()
        self.__height: int = height
        self.__width: int = width
        self.__begin_y: int = begin_y
        self.__begin_x: int = begin_x
        self.__win_texteditor: curses._CursesWindow = None
        self.__win_counter = None

        self.__ESC_KEY: int = 27
        self.__DEL_KEY: int = 127

    def input(self, stdscr) -> dict:
        # variables
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        GREEN: int = curses.color_pair(2)
        RED: int = curses.color_pair(3)

        # init windows
        stdscr.clear()
        self.__win_texteditor = curses.newwin(
            self.__height,
            self.__width,
            self.__begin_y,
            self.__begin_x
        )
        self.__win_counter = curses.newwin(
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
        target_words: int = 20
        words_count: int = 0
        escape_counter: int = 3

        text: str = ""

        self.__win_counter.clear()
        self.__win_counter.addstr(f'{words_count:03}/{target_words:03} words')
        win_msg.addstr(0, 0, f'Press ESC {escape_counter} times to exit', curses.A_DIM)
        win_msg.refresh()
        self.__win_counter.refresh()

        while True:
            key: int = self.__get()

            win_msg.clear()
            if chr(key) == ' ':
                words_count += 1
            if key == self.__ESC_KEY:
                escape_counter -= 1
                if words_count >= target_words or escape_counter == 0:
                    break
                else:
                    win_msg.addstr(0, 0, f'{target_words - words_count} more words to write', RED)
                    win_msg.addstr(1, 0, f'Press ESC {escape_counter} times to exit', curses.A_DIM)
            else:
                escape_counter = 3
            if words_count > target_words:
                win_msg.addstr(0, 0, f'Target words reached!\nExit by pressing ESC', GREEN)

            self.__print(key)
            if key != self.__DEL_KEY: # delete command
                text += chr(key)

            if chr(key).isspace():
                words_count += 1
            self.__win_counter.clear()
            self.__win_counter.bkgd(' ')
            self.__win_counter.addstr(f'{words_count:03}/{target_words:03} words')

            self.__win_counter.refresh()
            win_msg.refresh()
            self.__win_texteditor.refresh()

        Animation.load(self.__win_texteditor)
        return {"content": text, "words_count": words_count}

    def __print(self, text: str | int) -> None:
        if isinstance(text, int) and (text == 127 or text == 27):
            return
        if isinstance(text, int):
            text = chr(text)
        self.__win_texteditor.addstr(text)
        self.__win_texteditor.refresh()

    def __get(self) -> int:
        ascii_character = self.__win_texteditor.getch()
        return ascii_character

    # not used
    def getkey(self) -> chr:
        ascii_character: int = self.__win_texteditor.getch()
        return chr(ascii_character)

    # not used
    def get_and_print(self) -> None:
        character: chr = self.__get()
        self.__print(character)

    def __str__(self) -> str:
        return f"""
        width: {self.__width} | height: {self.__height}
        area: {self.__width * self.__height}
        margin: {self.__begin_y}(top), {self.__begin_x}(left)
        """

    # def __del__(self) -> None:
    #     curses.nocbreak()
    #     curses.echo()
    #     curses.endwin()


class Menu:

    def __init__(self) -> None:
        pass

    @staticmethod
    def select() -> str:

        def options(stdscr):

            """ called like this: mode = wrapper(Menu.select) """
            stdscr.clear()
            curses.curs_set(0)

            # curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
            # GRAY = curses.color_pair(1)
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
            GREEN: int = curses.color_pair(2)

            position: int = 0
            options: dict = {
                0: "note",
                1: "chat"
            }

            stdscr.addstr(1, 2, "NOTE", GREEN)
            stdscr.addstr(1, 8, "CHAT")
            stdscr.refresh()

            while True:
                rectangle(stdscr, 0, 0, 2, 14)

                ascii_ch: int = stdscr.getch()
                match ascii_ch:
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
        
        return curses.wrapper(options)


class Animation:

    def __init__(self):
        pass

    @staticmethod
    def load(screen, rounds=2, before='', after='') -> None:
        curses.curs_set(0)
        yx: tuple[int, int] = screen.getyx()
        frames: List[str] = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
        n: int = len(frames)
        for i in range(n * 2):
            screen.addstr(yx[0] + 1, 0, f'\r{frames[i % n]} saving')
            screen.refresh()
            sleep(0.1)

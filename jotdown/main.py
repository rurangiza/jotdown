""" Imports """
import sys
sys.path.append('/Users/fortytwo/Desktop/build/jotdown/jotdown/')

import time

from inout import prompt, stream, TextEditor, CurseWindow
from llm import Scribe, Librarian
from datetime import date
from curses import wrapper

from termcolor import colored

from typing import List


""" Configuration """

""" Code """

def main():

    librarian, scribe = Librarian(), Scribe()

    # weekday: int = date.today().weekday()
    # its_sunday: bool = True if weekday == 6 else False
    while True:
        try:
            mode: str = wrapper(CurseWindow.option_menu)
            if mode == "note":
                newnote: dict = scribe.record()
                librarian.store(newnote)
            else:
                while (question := prompt(">>> ")) != "exit!":
                    response = librarian.retrieve(question)
                    stream(response['answer'])
        except KeyboardInterrupt:
            break
        except EOFError:
            break


""" Execution """

if __name__ == "__main__":
    main()

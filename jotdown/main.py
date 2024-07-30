""" Imports """
import time

from inout import prompt, stream, TextEditor, CurseWindow
from llm import Scribe, Librarian
from datetime import date
from curses import wrapper

from typing import List


""" Configuration """


""" Code """

def main():

    librarian, scribe = Librarian(), Scribe()

    # weekday: int = date.today().weekday()
    # its_sunday: bool = True if weekday == 6 else False

    while True:
        mode: str = wrapper(CurseWindow.option_menu)
        match mode:
            case "note":
                note = scribe.record()
                # print(note)
                time.sleep(1)
                break
                # librarian.store(note)
            case _:
                print("What would you like to know?")
                while (question := prompt(": ")) != "exit!":
                    response = librarian.retrieve(question)
                    stream(response['answer'])


""" Execution """

if __name__ == "__main__":
    main()

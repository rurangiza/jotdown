""" Imports """
import sys
sys.path.append('/Users/fortytwo/Desktop/build/jotdown/jotdown/')

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
        try:
            mode: str = wrapper(CurseWindow.option_menu)
            if mode == "note":
                newnote: dict = scribe.record()
                # note = """
                # My favourite anime is Bleach. I've seen every episode and I plan on rewatching them.
                # Outside of anime I also enjoy watching rocket launches and eating japanese food.
                # """
                librarian.store(newnote)
            else:
                while (question := prompt(": ")) != "#soft-exit#":
                    response = librarian.retrieve(question)
                    stream(response['answer'])
        except KeyboardInterrupt:
            break


""" Execution """

if __name__ == "__main__":
    main()

""" Imports """
import time

from inout import prompt, stream, TextEditor
from llm import Scribe, Librarian
from curses import wrapper

from typing import List


""" Configuration """


""" Code """

def main():

    scribe, librarian = Scribe(), Librarian()

    while True:
        pick = wrapper(TextEditor.option_menu)
        if pick == "chat":
            print("What would you like to know?")
            while (question := prompt(": ")) != "exit!":
                response = librarian.retrieve(question)
                stream(response['answer'])
            exit(0)
        else:
            note = scribe.record()
            librarian.store(note)



""" Execution """

if __name__ == "__main__":
    main()

""" Imports """
import time

from inout import prompt, stream, TextEditor
from llm import Scribe, Librarian
from datetime import date
from curses import wrapper

from typing import List


""" Configuration """


""" Code """

def main():

    librarian = Librarian()

    if date.today().weekday() != 6: # it's not sunday
        print("--- It's not sunday, take notes.")
        scribe = Scribe()
        note = scribe.record()
        print(note)
        # librarian.store(note)
    else:
        print("--- It's sunday. Review your notes.")
        print("What would you like to know?")
        while (question := prompt(": ")) != "exit!":
            response = librarian.retrieve(question)
            stream(response['answer'])
        exit(0)



""" Execution """

if __name__ == "__main__":
    main()

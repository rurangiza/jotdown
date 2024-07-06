""" Imports """
import time

from inout import prompt, stream
from llm import Scribe, Librarian
from curses import wrapper

from typing import List


""" Configuration """


""" Code """

def main():

    scribe, librarian = Scribe(), Librarian()

    while True:
        res = input("Would you like to 'write' a note or 'chat'? ")
        if res == "chat":
            while (question := prompt(": ")) != "exit!":
                response = librarian.retrieve(question)
                stream(response['answer'])
            exit(0)
        else:
            note = scribe.record()
            time.sleep(1)
            stream(note)
            librarian.store(note)



""" Execution """

if __name__ == "__main__":
    main()

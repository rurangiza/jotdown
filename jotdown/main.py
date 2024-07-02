""" Imports """

from dotenv import load_dotenv, find_dotenv

from inout import prompt, stream
from llm import Cleaner, Scribe, Librarian

from typing import List


""" Configuration """

load_dotenv(find_dotenv())
MINIMUM_WORDS = 20

""" Code """


def main():

    cleaner, scribe, librarian = Cleaner(), Scribe(), Librarian()

    while True:
        res = input("Would you like to 'write' a note or 'chat'? ")
        if res == "chat":
            while (question := prompt(": ")) != "exit!":
                result = librarian.retrieve(question)
                print(result)
            exit(0)
        else:
            # note = Scribe.record()
            note = """
            Here is my plan to join Odoo
            1. I will learn data structures and algorithms
            2. I will solve 50 problems
            3. I will practice designing class diagrams + learn pre-requesites
            4. I will practice designing entity relation diagrams
            5. I will implement class diagrams in python
            6. I will implement ER diagrams in SQL
            """
            doc = librarian.store(note)
            print(">> Stored this document:\n", doc)


""" Execution """

if __name__ == "__main__":
    main()

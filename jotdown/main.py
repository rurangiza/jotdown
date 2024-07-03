""" Imports """

from inout import prompt, stream
from llm import Cleaner, Scribe, Librarian

from typing import List


""" Configuration """


""" Code """

def main():

    cleaner, scribe, librarian = Cleaner(), Scribe(), Librarian()

    while True:
        res = input("Would you like to 'write' a note or 'chat'? ")
        if res == "chat":
            while (question := prompt(": ")) != "exit!":
                response = librarian.retrieve(question)
                stream(response['answer'])
            exit(0)
        else:
            # note = Scribe.record()
            note = """
            A little about myself
            my favorite anime is One Piece and my favourite character
            is Zoro. In terms of music, I enjoy Hiphop & RnB.
            In my free time I play Mario Card, share drinks, watch movies
            and also produce music in my home studio at Ghlin. 
            """
            doc = librarian.store(note)
            print(">> Stored this document:\n", doc)


""" Execution """

if __name__ == "__main__":
    main()

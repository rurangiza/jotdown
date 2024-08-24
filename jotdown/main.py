""" Imports """

import os
import sys
import getpass

from datetime import date
from llm import Scribe, Librarian
from ui import Menu

from dotenv import load_dotenv


""" Configuration / Setup """

load_dotenv()
if not os.environ['OPENAI_API_KEY']:
    os.environ['OPENAI_API_KEY'] = getpass.getpass("Enter your OpenAI API key: ")


""" The fun begins """

def main():
    librarian, scribe = Librarian(), Scribe()

    # weekday: int = date.today().weekday()
    # its_sunday: bool = True if weekday == 6 else False

    demo_notes = [
        "my name is lupin. I live in Brussels, which is a city in Belgium",
        "I love watching anime, my favourite is One Piece, because I love travelling on boats",
        "my favourite music are soul music, hip-hop, jazz and electronic. i can play the keyboard and I use Ableton as my D.A.W",
        "I've travelled to a few places. Malta, Croatia, England and Norway"
    ]

    try:
        args = sys.argv
        if len(args) == 2 and args[1] == "demo":
            for note in demo_notes:
                librarian.store({"content": note, "words_count": len(note.split())})
            librarian.chat()
        else:
            while True:
                if Menu.select() == "chat":
                    librarian.chat()
                else:
                    note: dict = scribe.record()
                    librarian.store(note)
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass
    except Exception as e:
        with open("logs.txt", "a") as f:
            f.write(f'- UNEXPECTED ERROR: {e} | {str(date.today())}')

if __name__ == "__main__":
    main()

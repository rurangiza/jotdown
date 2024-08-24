""" Imports """

import os
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
    # weekday: int = date.today().weekday()
    # its_sunday: bool = True if weekday == 6 else False
    pick = Menu.select()
    try:
        librarian = Librarian()
        if pick == "chat":
            librarian.chat()
        else:
            scribe = Scribe()
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

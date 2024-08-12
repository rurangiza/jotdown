import os
import sys
import time
import getpass
from llm import Scribe, Librarian
from datetime import date

sys.path.append('/Users/fortytwo/Desktop/build/jotdown/jotdown/')


def main():

    # Setup
    if not os.environ['OPENAI_API_KEY']:
        os.environ['OPENAI_API_KEY'] = getpass.getpass("OpenAI API key: ")

    # app
    weekday: int = date.today().weekday()
    its_sunday: bool = True if weekday == 6 else False
    try:
        librarian = Librarian()
        if not its_sunday:
            librarian.chat()
        else:
            scribe = Scribe()
            newnote: dict = scribe.take_notes()
            librarian.store(newnote)            
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass
    except Exception as e:
        print(f'Unexpected Error: {e}')
        time.sleep(2)

""" Execution """

if __name__ == "__main__":
    main()

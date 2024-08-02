import sys
import time
sys.path.append('/Users/fortytwo/Desktop/build/jotdown/jotdown/')
from llm import Scribe, Librarian
from datetime import date
from typing import List


""" Code """


def main():

    weekday: int = date.today().weekday()
    its_sunday: bool = True if weekday == 6 else False
    try:
        librarian = Librarian()
        if its_sunday:
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

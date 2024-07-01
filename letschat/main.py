""" Imports """

from dotenv import load_dotenv, find_dotenv

from inout import prompt, stream
from llm import LLM, Cleaner, Librarian

from typing import List


""" Configuration """

load_dotenv(find_dotenv())
llm = Cleaner()


""" Code """

def main():
    # if first time -> onboarding steps
    # else, if weekdays -> review
    # else, if sunday -> review the week


    """ Get the entry """
    stream("How was your day?")
    user_input: List[str] = []
    try:
        while "exit!" != (ans := prompt("...")):
            user_input.append(ans)
    except EOFError as _:
        pass
    entry = "\n".join(user_input)

    """ Summarize it using chatGPT """
    if not entry:
        return
    res = llm.clean(entry)
    stream(res)

""" Execution """

if __name__ == "__main__":
    main()

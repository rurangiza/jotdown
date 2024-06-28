""" Imports """
from logger import Logger as Log

""" Configurations """

""" Code """


def prompt(message: str, expected_input=str) -> str:
    ans = ""
    try:
        while not ans:
            ans = input(f"{message}: ")
        Log.info(ans)
        return ans
    except KeyboardInterrupt as _:
        Log.warning("exited: Ctrl^C pressed")
    except EOFError as _:
        Log.warning("exited: Ctrl^D pressed")


def main():
    prompt("Enter something")


""" Execution """

if __name__ == "__main__":
    main()
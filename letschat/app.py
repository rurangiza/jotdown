""" Imports """

from inout import prompt, stream


""" Code """


def main():
    # if first time -> onboarding steps
    # else, if weekdays -> review
    # else, if sunday -> review the week
    print("How was your day?")
    entry = []
    try:
        while "i'm done!" != (ans := prompt("...")):
            entry.append(ans)
    except EOFError as e:
        print("\nEnd of chat")
    print("----- your entry ----")
    stream("\n".join(entry))


""" Execution """

if __name__ == "__main__":
    main()

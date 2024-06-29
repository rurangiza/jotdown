""" Imports """

from inout import prompt, stream


""" Code """

def main():
    print("How was your day?")
    entry = []
    while "i'm done!" != (ans := prompt("...")):
        entry.append(ans)

    print("----- your entry ----")
    stream("\n".join(entry))


""" Execution """

if __name__ == "__main__":
    main()
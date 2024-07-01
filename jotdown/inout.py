""" Handling user input and output """

from time import sleep

def prompt(message: str) -> str:
    """
    Taking user input
    --
    :param message: prompt message
    :return: str, valid user input
    """
    ans = ""
    count = 2
    while not ans:
        if count == 0:
            raise EOFError
        try:
            ans = input(f"{message} ")
        except KeyboardInterrupt as _:
            break
        count -= 1
    return ans


def stream(message: str, chunk_size=3, delay=0.1) -> None:
    """
    Printing the message 3 characters at a time
    --
    :param message : text message to print be printed
    :param chunk_size : size of each chunk
    :param delay (float)
    :return: None
    """
    n = len(message)
    for i in range(0, n, chunk_size):
        print(message[i:i+chunk_size], end="", flush=True)
        sleep(delay)
    print("")


def loader():
    animation = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
    idx = 0
    while True:
        print(animation[idx % len(animation)], end="\r")
        idx += 1
        sleep(0.1)

def greet():
    print("Hello, World!")
import sys
from color import Color


def user_input(str: str):
    try:
        query = input(Color.GREEN + str).rstrip()
        print(Color.END)
        return query
    except KeyboardInterrupt:
        print(Color.RED + "\n入力が中断されました" + Color.END)
        sys.exit(1)


def llm_print(str: str):
    print(Color.BLUE + str + Color.END)


def event_print(str: str):
    print(Color.GRAY + str + Color.END)


def error_print(str: str):
    print(Color.RED + str + Color.END)

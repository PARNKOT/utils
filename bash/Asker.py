import typing
import getpass


class Asker:
    @staticmethod
    def ask(msg: str, validate: typing.Callable = lambda arg: bool(arg), default: typing.Any = None):
        answer = input(msg)
        return answer if validate(answer) else default

    @staticmethod
    def ask_yes_no(msg, default=None):
        answer = Asker.ask(msg,
                           validate=lambda answer: answer.lower() in ['y', 'n', 'yes', 'no'],
                           default=default)
        return True if answer.lower()[0] == 'y' else False

    @staticmethod
    def ask_password(msg):
        password = getpass.getpass(prompt=msg)
        if password == "":
            print("\nWARNING: empty password!\n")
        return password

    @staticmethod
    def select(msg: str, selection: typing.Sequence):
        print(msg)
        for index, var in enumerate(selection):
            print(f"{index}: {var}")
        choice = int(input(f"Your selection (0-{len(selection) - 1}): "))
        return selection[choice]

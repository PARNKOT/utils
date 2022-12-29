import getpass
import os
import re


def is_root_user():
    return os.getuid() == 0


def replace_in_file(file_path, old, new):
    found_count = 0
    with open(file_path, "r+") as file:
        lines = []
        for line in file:
            if re.match(f"^{old}", line):
                lines.append(line.replace(old, new))
                found_count += 1
            else:
                lines.append(line)
        file.seek(0)
        file.writelines(lines)
    return found_count


def read_variable_from(file_path: str, var: str) -> str:
    with open(file_path, "r") as file:
        for line in file:
            if re.match(f"^{var}=", line):
                return line.strip().split('=')[1]

    raise ValueError(f"Variable {var} does not exist")


def debug(msg: str):
    print(msg)
    while input("Press \"Enter\" to continue: ") != "":
        pass


if __name__ == "__main__":
    pass

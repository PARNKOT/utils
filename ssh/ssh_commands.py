
from bash.shell_commands import shell_run_command
from ssh.SSH import SSH


def run_ssh_command(host: str, cmd: str):
    return shell_run_command(f"ssh -t {host} \"{cmd}\"")


def copy_ssh_id(ssh_host: str):
    return shell_run_command(f"ssh-copy-id {ssh_host}")


def disable_password_asking(host_addr: str, password: str, sudoers_file: str):
    cmd = f"echo \'%sudo ALL=(ALL) NOPASSWD:ALL\' | sudo tee {sudoers_file}"

    with SSH(host_addr, password) as conn:
        while conn.run_command_with_password(cmd):
            if input("Try again? (Y/n): ").lower()[0] == "n":
                return False
    return True
    #while run_ssh_command_with_password(host_addr, password, cmd):
    #    if input("Try again? (Y/n): ").lower()[0] == "n":
    #        return False
    #    #password = getpass.getpass("Type password manually: ")
    #return True


if __name__ == "__main__":
    pass

import re
import time
import paramiko


class SSH:
    def __init__(self, ssh_addr: str, password=''):
        self.ssh_addr = ssh_addr
        self.user, self.addr = ssh_addr.split('@')
        self.__password = password
        self.__client = paramiko.SSHClient()
        self.__channel = None
        self.last_command_exit_status: int = 0

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__channel.close()
        self.__client.close()

    def connect(self):
        self.__client = paramiko.SSHClient()
        self.__client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if self.__password:
            self.__client.connect(hostname=self.addr, username=self.user, password=self.__password, allow_agent=True)
        else:
            self.__client.connect(hostname=self.addr, username=self.user, allow_agent=True)

        self.__channel = self.__client.get_transport().open_session()
        self.__channel.get_pty()
        self.__channel.setblocking(True)

    def run_command(self, cmd: str) -> bool:
        stdin, stdout, stderr = self.__client.exec_command(cmd)
        out_lines = stdout.readlines()
        for line in out_lines:
            print(self.addr, ":", line.strip())
        return len(out_lines) > 0

    def run_command_with_password(self, cmd: str):
        self.__channel.exec_command(cmd)

        stdout = b''
        while not self.__channel.recv_ready():
            stdout = self.__channel.recv(4096)
            if re.search('[Pp]assword', stdout.decode()):
                self.__channel.send((self.__password + '\n').encode())
            time.sleep(1)

        while self.__channel.recv_ready():
            stdout += self.__channel.recv(4096)
        self.last_command_exit_status = self.__channel.exit_status
        print(self.addr, stdout.decode())
        return self.last_command_exit_status


if __name__ == "__main__":
    pass
    #with SSH("egor@localhost", "123") as conn:
    #    print(conn.run_command("uname -a"))
        #conn.run_command_with_password("sudo cat /etc/sudoers")

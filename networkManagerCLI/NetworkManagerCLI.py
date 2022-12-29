import subprocess
import typing
from utils.shell_commands import shell_run_command


class Connection:
    def __init__(self, con_name, ifname='', autoconnect=False, type='', ip4='', gw4='', uuid=''):
        self.con_name: str = con_name
        self.ifname: str = ifname
        self.autoconnect: bool = autoconnect
        self.type: str = type  # ethernet | bridge | wifi | ...
        self.ip4: str = ip4
        self.gw4: str = gw4
        self.UUID: str = uuid
        self.method: str = ''  # auto | manual
        self.dns = set()

    def as_add_str(self):
        add_string = f"con-name \"{self.con_name}\" "
        if self.ifname:
            add_string += f"ifname \"{self.ifname}\" "
        if self.autoconnect:
            add_string += f"autoconnect yes "
        if self.type:
            add_string += f"type {self.type} "
        if self.ip4:
            add_string += f"ip4 \"{self.ip4}\" "
        if self.gw4:
            add_string += f"ifname \"{self.gw4}\" "

        return add_string

    def as_modify_str(self):
        modify_string = ""
        if self.UUID:
            modify_string += f"\"{self.UUID}\" "
            modify_string += f"connection.id {self.con_name} "
        else:
            modify_string += f"{self.con_name} "
        if self.method:
            modify_string += f"ipv4.method \"{self.method}\" "
        if self.ip4:
            modify_string += f"ipv4.addresses \"{self.ip4}\" "
        if self.gw4:
            modify_string += f"ipv4.gateway \"{self.gw4}\" "
        if self.dns:
            modify_string += f"ipv4.dns \"{' '.join(self.dns)}\" "
        if self.autoconnect:
            modify_string += f"connection.autoconnect yes "
        return modify_string

    def __eq__(self, other):
        return self.ifname == other.ifname


class NetworkManagerCLI:

    @staticmethod
    def add_connection(conn: Connection):
        return shell_run_command(f"nmcli connection add {conn.as_add_str()}")

    @staticmethod
    def up_connection(conn_uuid: str):
        return shell_run_command(f"nmcli connection up \"{conn_uuid}\" ")

    @staticmethod
    def down_connection(conn_uuid: str):
        return shell_run_command(f"nmcli connection down \"{conn_uuid}\" ")

    @staticmethod
    def modify_connection(conn: Connection):
        shell_run_command(f"nmcli connection modify {conn.as_modify_str()}")

    @staticmethod
    def get_connections() -> typing.List[Connection]:
        process = subprocess.Popen(["nmcli connection show"], shell=True, stdout=subprocess.PIPE)
        stdout, _ = process.communicate()
        process.wait()
        return NetworkManagerCLI.__parse_connections(stdout.decode().strip())

    @staticmethod
    def __parse_connections(connections: str) -> typing.List[Connection]:
        connections_parsed = []
        for connection_str in connections.split('\n')[1:]:
            *name, uuid, type, ifname = connection_str.split()
            connections_parsed.append(Connection(' '.join(name), ifname, type=type, uuid=uuid))
        return connections_parsed


if __name__ == "__main__":
    for connection in NetworkManagerCLI.get_connections():
        print(connection.ifname)
    conn = Connection('External')
    conn.ifname = 'eno1'
    conn.autoconnect = True
    conn.type = 'ethernet'
    conn.ip4 = '10.1.1.144'
    conn.gw4 = '10.1.1.253'
    conn.UUID = "123"

    print(conn.as_modify_str())

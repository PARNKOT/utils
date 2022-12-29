import subprocess
import apt


def shell_run_command(cmd: str):
    process = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line.strip())
    process.wait()
    return process.returncode


def ping(host: str):
    return shell_run_command(f'ping -c 1 {host}')


def apt_get(command: str, params='', args=''):
    return shell_run_command(f'apt-get {command} {params} {args}')


def netplan_apply():
    return shell_run_command("netplan apply")


def systemctl_enable(*services):
    return shell_run_command(f"systemctl enable {' '.join(services)}")


def systemctl_start(*services):
    return shell_run_command(f"systemctl start {' '.join(services)}")


def systemctl_restart(*services):
    return shell_run_command(f"systemctl restart {' '.join(services)}")


def date_universal():
    process = subprocess.Popen(["date --universal +\"%s\""], shell=True, stdout=subprocess.PIPE)
    return process.stdout.read().decode().strip('\n')


def apt_update():
    return apt.cache.Cache().update()


def apt_upgrade():
    return apt.cache.Cache().upgrade()


def apt_install(*packages):
    cache = apt.cache.Cache()
    cache.update()
    cache.open()
    for pkg_name in packages:
        pkg = cache[pkg_name]
        if pkg.is_installed:
            print(f"{pkg_name} already installed")
        else:
            pkg.mark_install()

            try:
                cache.commit()
            except Exception as e:
                print(f"Sorry, package installation failed\n {e}")


def is_computer_online(host: str):
    return False if ping(host) else True


if __name__ == "__main__":
    pass  # shell_run_command_with_password("ssh-copy-id egor@10.1.1.239", "123")



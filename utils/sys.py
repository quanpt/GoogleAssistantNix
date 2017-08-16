from subprocess import check_output, CalledProcessError


def get_pid(name):
    try:
        return int(check_output(["pidof",name]).decode('utf-8'))
    except CalledProcessError:
        return -1
import subprocess as sp


def run_cmd(*args, timeout=10) -> str:
    p = sp.Popen([*args], stdout=sp.PIPE)
    p.wait(timeout)
    return p.stdout.read().decode('utf-8')
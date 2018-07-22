import subprocess as sp


def run_cmd(*args) -> str:
    p = sp.Popen([*args], stdout=sp.PIPE)
    p.wait(1)
    return p.stdout.read().decode('utf-8')
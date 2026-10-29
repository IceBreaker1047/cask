'''
Usage:
    running:
        python spawn.py run /bin/sh
    will:
        -fork a new process which will run /bin/sh
        -parent will wait for the process to finish
'''

import os
import click
import traceback

#Group all the subcommands under the cli command
@click.group()
def cli():
    pass

@cli.command()
@click.argument('command', required=True, nargs=-1)
def run(command):
    pid = os.fork()
    #child process
    if pid==0:
        try:
            contain(command)
        except Exception:
            traceback.print_exc()
            os._exit(1)
    else:
        _,status = os.waitpid(pid, 0)
        print(f"Process {pid} exited with status {status}")

#Replace the current child process with the command
def contain(command):
    os.execvp(command[0], command)
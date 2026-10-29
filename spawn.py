'''
Usage:
    running:
        python spawn.py run /bin/sh
    will:
        -fork a new process
        -unpack ubuntu libraries in new directory
        -chroot() the process in the new directory
        -exec /bin/sh
        -parent will wait for the process to finish
'''

import os
import click
import traceback
import tarfile
import uuid

def _get_image_path(image_name, image_dir, image_suffix='tar'):
    return os.path.join(image_dir, os.extsep.join([image_name, image_suffix]))

def _get_container_path(container_id, container_dir, *subdir_names):
    return os.path.join(container_dir, container_id, *subdir_names)

#Create container root by extracting an image into a new directory
def create_container_root(image_name, image_dir, container_id, container_dir):
    image_path = _get_image_path(image_name, image_dir)
    container_root = _get_container_path(container_id, container_dir, 'rootfs')

    assert os.path.exists(image_path), "unable to locate the %s" % image_name

    if not os.path.exists(container_root):
        os.makedirs(container_root)

    with tarfile.open(image_path) as t:
        members = [m for m in t.getmembers() 
                   if m.type not in (tarfile.CHRTYPE, tarfile.BLKTYPE)]
        t.extractall(container_root, members=members)

    return container_root

#Group all the subcommands under the cli command
@click.group()
def cli():
    pass

BASE_DIR = os.environ.get('SPAWN_HOME', '/var/lib/spawn')
DEFAULT_IMAGE_DIR = os.path.join(BASE_DIR, 'images')
DEFAULT_CONTAINER_DIR = os.path.join(BASE_DIR, 'containers')

@cli.command()
@click.option('--image-name', '-i', default='ubuntu')
@click.option('--image-dir', '-d', default=DEFAULT_IMAGE_DIR)
@click.option('--container-dir', '-c', default=DEFAULT_CONTAINER_DIR)
@click.argument('command', required=True, nargs=-1)
def run(command, image_name, image_dir, container_dir):
    container_id = str(uuid.uuid4())
    pid = os.fork()
    #child process
    if pid==0:
        try:
            contain(command, image_name, image_dir, container_id, container_dir)
        except Exception:
            traceback.print_exc()
            os._exit(1)
    else:
        _,status = os.waitpid(pid, 0)
        print(f"Process {pid} exited with status {status}")

#Replace the current child process with the command
def contain(command, image_name, image_dir, container_id, container_dir):
    #Create the container root
    root = create_container_root(image_name, image_dir, container_id, container_dir)
    print(f"Created new root for the container at {root}")

    os.chroot(root)
    os.chdir('/')
    os.execvp(command[0], command)

if __name__ == '__main__':
    cli()
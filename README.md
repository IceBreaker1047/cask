# CASK

A minimal Docker style container runtime written in Python. It unpacks a root filesystem image and runs a command inside it using Linux `chroot`.

## Requirements

- Linux. On Windows/macOS, use a Linux VM or WSL2.
- Root privileges (`sudo`)
- Python 3.9+

## Setup

**1. Clone the repo**

```bash
git clone https://github.com/IceBreaker1047/cask
cd cask
```

**2. Create the image folder**

```bash
sudo mkdir -p /var/lib/spawn/images
```

**3. Get a root filesystem image**

CASK needs a rootfs tarball. Alpine's minirootfs is tiny (~3 MB) and works well:

```bash
FILE=$(curl -s https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/x86_64/ | grep -o 'alpine-minirootfs-[0-9.]*-x86_64.tar.gz' | sort -u | tail -1)
wget https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/x86_64/$FILE
```

**4. Install it under the name CASK expects**

```bash
sudo cp alpine-minirootfs-*-x86_64.tar.gz /var/lib/spawn/images/alpine.tar
```

The filename must be `<image_name>.tar`. Any rootfs tarball works, as long as it is named this way.

## Usage

```bash
sudo python3 spawn.py run -i alpine /bin/sh
```

You should land in a shell inside the Alpine rootfs. Verify with:

```bash
cat /etc/os-release
```

Type `exit` to leave the container.

### Options

| Option | Short | Default | Description |
|---|---|---|---|
| `--image-name` | `-i` | `ubuntu` | Image to run (`<image-dir>/<name>.tar`) |
| `--image-dir` | `-d` | `/var/lib/spawn/images` | Where image tarballs live |
| `--container-dir` | `-c` | `/var/lib/spawn/containers` | Where container filesystems are created |

Set `SPAWN_HOME` to change the base directory:

```bash
sudo SPAWN_HOME=/data/spawn python3 spawn.py run -i alpine /bin/sh
```
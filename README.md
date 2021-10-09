# photolink

**photolink** is a Python script that reflects the structure of your photo collection to the file system using hard links.

The idea is that you can browse your photos by events and tags using any application without consuming any extra disk space.

Currently, it extracts the photo collection from a [Shotwell](https://github.com/GNOME/shotwell) SQLite database, but other sources can be added later.

Then it creates **_events** and **_tags** directories under the specified base path. Each photo that belongs to a tag or an event is then hard-linked into a subdirectory of **_tags** or **_events** correspondingly. Events always have a flat structure, while tags can be nested.

## Usage
```
usage: photolink [-h] [-v] [-n] path

Organize photos by events and tags using hard links

positional arguments:
  path           the base path for _events and _tags directories, created if
                 doesn't exist

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print a message for each directory and link created
  -n, --dry-run  iterate over the photo collection, but don't make any changes
                 to the file system; useful with -v to see what would be done
```

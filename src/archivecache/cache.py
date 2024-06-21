import os
import time
import random
import pathlib

from archivecache import tabletree

cache_directory = "cache/"


# NOTE: It should be possible to delete the cached files without causing failure. Missing cached files will be downloaded again if possible.

# NOTE: Guessing cache keys and injecting them in to directory files is a potential attack vector.


def new_key():
    time.sleep(0.001)  # Wait for it!

    return (
        "{:0.20f}".format(time.time()) + "{:.50f}".format(random.random())[1:]
    ).replace(
        ".", ""
    )  # + '.bin'


def full_file_path(cache_key):
    filename = "".join([c for c in cache_key if c.isalpha() or c.isdigit()])

    return os.path.join(cache_directory, filename)


def exists(cache_key):
    return pathlib.Path(full_file_path(cache_key)).exists()


def new_temporary():
    return tabletree.Component().get(["temporary", new_key()], create=True)


#

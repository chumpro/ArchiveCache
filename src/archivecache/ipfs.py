import subprocess
import urllib.request
import urllib.parse
import json

from archivecache import cache

ipfs_api_server = "127.0.0.1:5001"


def cat(file_hash):
    url = "http://%s/api/v0/cat" % ipfs_api_server

    with urllib.request.urlopen(url + "?arg=" + file_hash, "".encode("ascii")) as f:
        return f.read()


def copy_to_cache(file_hash):
    cache_key = cache.new_key()

    if not cache.exists(cache_key):
        subprocess.run(
            [
                "ipfs",
                "get",
                "--output",
                cache.full_file_path(cache_key),
                "--",
                file_hash,
            ]
        )

    return cache_key


def copy_from_cache(cache_key):
    result = subprocess.run(
        ["ipfs", "add", "-Q", cache.full_file_path(cache_key)], capture_output=True
    )

    return result.stdout.decode("utf-8").strip()


def get_size(file_hash):
    url = "http://%s/api/v0/ls" % ipfs_api_server

    with urllib.request.urlopen(url + "?arg=" + file_hash, "".encode("ascii")) as f:
        result = f.read()

    r = json.loads(result)

    links = r["Objects"][0]["Links"]

    if len(links) == 0:
        return None

    size = sum([int(x["Size"]) for x in links])

    return size


#

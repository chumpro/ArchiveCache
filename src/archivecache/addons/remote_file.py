import os
import pyfuse3
import stat


from archivecache.addons import remote_data
from archivecache import database, tabletree, ipfs, cache, version


version.require(0, 0)


def new(base):
    profile = base.get(".policy")

    if profile and profile.get_value() == "remote_file_v0":
        return AddonComponent(base.node_id)


class AddonComponent(remote_data.AddonComponent):
    def __init__(self, node_id):
        super().__init__(node_id)

        self.size = self.get_size()

    def fs_is_directory(self):
        return False

    def get_size(self):
        cache_key = self.get_data_at(".cache")

        if cache_key is not None:
            try:
                return os.path.getsize(cache.full_file_path(cache_key))

            except FileNotFoundError:
                return 0

        ipfs_hash = self.get_hash()

        if ipfs_hash is not None:
            size = ipfs.get_size(ipfs_hash)

            if size is not None:
                return size

            else:
                self.download_remote_file()  # Note: This only happens for small files.

                return self.get_size()

    def fs_data_size(self):
        return self.size

    def fs_attributes(self):
        entry = pyfuse3.EntryAttributes()

        entry.st_mode = stat.S_IFREG | 0o644

        entry.st_size = self.fs_data_size()

        stamp = int(1438467123.985654 * 1e9)

        entry.st_atime_ns = stamp

        entry.st_ctime_ns = stamp

        entry.st_mtime_ns = stamp

        entry.st_gid = os.getgid()

        entry.st_uid = os.getuid()

        entry.st_ino = self.get_id()

        return entry

    def fs_open(self):
        self.download_remote_file()

    def fs_read(self, offset, length):
        self.download()

        cache_key = self.get_data_at(".cache")

        with open(cache.full_file_path(cache_key), "r") as f:
            f.seek(offset)

            return f.read(length).encode()

        raise pyfuse3.FUSEError(errno.EACCES)

    def fs_write(self, offset, buffer):
        cache_key = self.get_data_at(".cache")

        if cache_key is not None:
            with open(cache.full_file_path(cache_key), "wb") as f:
                f.seek(offset)

                f.write(buffer)

                self.size = len(buffer)

            self.rehash()

            return self.size

        raise pyfuse3.FUSEError(errno.EACCES)

    def upload(self):
        if self.get(".ipfs_hash") is None:
            cache_key = self.get_data_at(".cache")

            if cache_key is not None:
                ipfs_hash = ipfs.copy_from_cache(cache_key)

                self.set({".ipfs_hash": ipfs_hash})

    def download(self):
        pass

    def download_remote_file(self):
        if self.get(".cache") is None:
            ipfs_hash = self.get_hash()

            if ipfs_hash is not None:
                cache_key = ipfs.copy_to_cache(ipfs_hash)

                self.set({".cache": cache_key})

    def get_reference(self):
        return {
            ".policy": self.get_data_at(".policy"),
            ".ipfs_hash": self.get_hash(),
        }


#

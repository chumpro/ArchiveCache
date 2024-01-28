import json
import os
import stat
import pyfuse3

from archivecache.addons import remote_data
from archivecache import database, tabletree, cache, ipfs, version, packet


version.require(0, 0)


def new(base):
    profile = base.get(".policy")

    if profile and profile.get_value() == "remote_directory_v0":
        return AddonComponent(base.node_id)


class AddonComponent(remote_data.AddonComponent):
    def fs_readdir(self):
        self.download()

    def fs_is_directory(self):
        return True

    def fs_data_size(self):
        return 0

    def fs_attributes(self):
        entry = pyfuse3.EntryAttributes()

        entry.st_mode = stat.S_IFDIR | 0o755 # TODO: Adjust access bits according to ownership.

        entry.st_size = self.fs_data_size()

        stamp = int(1438467123.985654 * 1e9)

        entry.st_atime_ns = stamp

        entry.st_ctime_ns = stamp

        entry.st_mtime_ns = stamp

        entry.st_gid = os.getgid()

        entry.st_uid = os.getuid()

        entry.st_ino = self.node_id

        return entry

    def fs_create(self, key, mode, flags, ctx):
        cache_key = cache.new_key()

        new_component = self.get(key, create=True)

        new_component.set({".policy": "remote_file_v0", ".cache": cache_key})

        path = cache.full_file_path(cache_key)

        open(path, "w").close()

        new_component.rehash()

        node_id = new_component.get_id()

        return node_id

    def fs_mkdir(self, key, mode, ctx):
        new_component = self.get(key, create=True)

        new_component.set({".policy": "remote_directory_v0"})

        new_component.rehash()

        node_id = new_component.get_id()

        return node_id

    def get_content(self):
        return {
            n.get_key(): n.get_reference()
            for n in self.get_nodes()
            if n.get_key() not in [".ipfs_hash", ".cache"]
        }

    def set_content(self, mapping):
        [self.get(k, create=True).set(v) for k, v in mapping.items()]

        # TODO: self.rehash()

    def upload(self):
        if self.get(".ipfs_hash") is None:
            self.upload_nodes()

            cache_key = (
                cache.new_key()
            )  # TODO: Creates a new cache file even when not needed. Delete old cache file if it exists.

            with open(cache.full_file_path(cache_key), "wb") as f:
                message = packet.data_to_message(self.get_content())

                f.write(message)

            ipfs_hash = ipfs.copy_from_cache(cache_key)

            self.set({".ipfs_hash": ipfs_hash, ".cache": cache_key})

    def download(self):
        if self.get(".cache") is None:
            ipfs_hash = self.get_hash()

            if ipfs_hash is not None:
                cache_key = ipfs.copy_to_cache(ipfs_hash)

                with open(cache.full_file_path(cache_key), "rb") as f:
                    message = f.read()

                    data = packet.message_to_data(message)

                    self.set_content(data)

                    self.set({".cache": cache_key})

    def get_content(self):
        return {
            n.get_key(): n.get_reference()
            for n in self.get_nodes()
            if n.get_key() not in [".ipfs_hash", ".cache", ".signature", ".owner"]
        }

    def get_reference(self):
        self.upload()

        return {
            n.get_key(): n.get_reference()
            for n in self.get_nodes()
            if n.get_key() in [".policy", ".ipfs_hash", ".signature", ".owner"]
        }

    def merge(self, component):
        component.download()

        identity_hash = self.get_data_at(".owner")

        if (
            identity_hash is not None
        ):  # Note: If there is an owner, and it is correct, replace everything.
            if component.verify_signature():
                if self.get(".owner").get_data() == component.get(".owner").get_data():
                    self.clear().set_content(component.get_data())

        else:  # Note: If there is no owner, add/merge. Do not allow setting owner.
            if component.get(".owner") is None:
                for component_node in component.get_nodes():
                    key = component_node.get_key()

                    node = self.get(key)

                    if node is None:  # Note: If the key is new, reference the content.
                        self.get(key, create=True).set(component_node.get_reference())

                    else:
                        node.merge(
                            component_node
                        )  # Note: If the key exists, attempt to merge.

        # TODO: self.rehash()


#

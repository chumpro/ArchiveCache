import os
import pyfuse3
import stat

from archivecache import database, tabletree, version


version.require(0, 0)


def new(base):
    if base.get_value() is None:
        return AddonComponent(base.node_id)


class AddonComponent(tabletree.TableTree):
    def __init__(self, node_id):
        super().__init__(node_id)

    def fs_is_directory(self):
        return True

    def fs_data_size(self):
        return 0

    def fs_attributes(self):
        entry = pyfuse3.EntryAttributes()

        entry.st_mode = stat.S_IFDIR | 0o755

        entry.st_size = self.fs_data_size()

        stamp = int(1438467123.985654 * 1e9)

        entry.st_atime_ns = stamp

        entry.st_ctime_ns = stamp

        entry.st_mtime_ns = stamp

        entry.st_gid = os.getgid()

        entry.st_uid = os.getuid()

        entry.st_ino = self.node_id

        return entry

    def get_reference(self):
        return {node.get_key(): node.get_reference() for node in self.get_nodes()}


#

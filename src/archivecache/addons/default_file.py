import os
import pyfuse3
import stat

from archivecache import tabletree, version


version.require(0, 0)


def new(base):
    return AddonComponent(base.node_id)


class AddonComponent(tabletree.TableTree):
    def __init__(self, node_id):
        super().__init__(node_id)

    def fs_is_directory(self):
        return False

    def fs_data_size(self):
        return len(str(self.get_value()))

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

        entry.st_ino = self.node_id

        return entry

    def fs_read(self, offset, length):
        return str(self.get_value()).encode()[offset : offset + length]

    def get_reference(self):
        return self.get_value()


#

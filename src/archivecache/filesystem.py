import os
import sys
import stat
import errno
import pyfuse3
import trio

from archivecache import tabletree, database, cache


try:
    import faulthandler

except ImportError:
    pass

else:
    faulthandler.enable()


def filename_to_key(filename):
    return filename.decode()


class ArchiveCacheFS(pyfuse3.Operations):
    enable_writeback_cache = False

    def __init__(self):
        super(ArchiveCacheFS, self).__init__()

    async def getattr(self, inode, ctx=None):
        component = tabletree.Component(inode)

        if component.exists():
            return component.fs_attributes()

        raise pyfuse3.FUSEError(errno.ENOENT)

    async def lookup(self, parent_inode, name, ctx=None):
        key = filename_to_key(name)

        parent_component = tabletree.Component(parent_inode)

        if parent_component.exists():
            component = parent_component.get(key)

            if component is not None:
                return await self.getattr(component.get_id())

        raise pyfuse3.FUSEError(errno.ENOENT)

    async def opendir(self, inode, ctx):
        # TODO: Verify that directory exists, handle root directory.

        return inode

    async def readdir(self, fh, start_id, token):
        component = tabletree.Component(fh)

        if component.exists():
            component.fs_readdir()

            # TODO: Sort inodes and keys to make sure that continue with start_id works as required.

            do_reply = start_id == 0

            for key, inode in zip(component.get_keys(), component.get_ids()):
                if inode is not None:
                    if do_reply:
                        r = pyfuse3.readdir_reply(
                            token,
                            key.encode(),
                            await self.getattr(inode),
                            inode,
                        )

                do_reply = do_reply or (inode == start_id)

            return

        raise pyfuse3.FUSEError(errno.ENOENT)

    async def open(self, inode, flags, ctx):
        component = tabletree.Component(inode)

        if component.exists():
            component.fs_open()

            return pyfuse3.FileInfo(fh=inode)

        raise pyfuse3.FUSEError(errno.ENOENT)

    async def read(self, fh, offset, size):
        component = tabletree.Component(fh)

        if component.exists():
            data = component.fs_read(offset, size)

            if data is not None:
                return data

        raise pyfuse3.FUSEError(errno.EACCES)

    async def write(self, fh, offset, buffer):
        component = tabletree.Component(fh)

        if component.exists():
            number_of_bytes_written = component.fs_write(offset, buffer)

            return number_of_bytes_written

        raise pyfuse3.FUSEError(errno.EACCES)

    async def create(self, parent_inode, name, mode, flags, ctx):
        parent_component = tabletree.Component(parent_inode)

        if parent_component.exists():
            key = filename_to_key(name)

            new_id = parent_component.fs_create(key, mode, flags, ctx)

            return pyfuse3.FileInfo(fh=new_id), await self.getattr(new_id)

        raise pyfuse3.FUSEError(errno.EACCES)

    async def mkdir(self, inode_p, name, mode, ctx):
        parent_component = tabletree.Component(inode_p)

        if parent_component.exists():
            key = filename_to_key(name)

            new_id = parent_component.fs_mkdir(key, mode, ctx)

            return await self.getattr(new_id)

        raise pyfuse3.FUSEError(errno.EACCES)

    async def rmdir(self, inode_p, name, ctx):
        parent_component = tabletree.Component(inode_p)

        if parent_component.exists():
            key = filename_to_key(name)

            result = parent_component.fs_unlink(key)

            if result:
                return

        raise pyfuse3.FUSEError(errno.EACCES)

    async def unlink(self, inode_p, name, ctx):
        parent_component = tabletree.Component(inode_p)

        if parent_component.exists():
            key = filename_to_key(name)

            result = parent_component.fs_unlink(key)

            if result:
                return

        raise pyfuse3.FUSEError(errno.EACCES)


def mount_fs(mountpoint):
    acfs = ArchiveCacheFS()

    fuse_options = set(pyfuse3.default_options)

    fuse_options.add("fsname=ArchiveCache")

    pyfuse3.init(acfs, mountpoint, fuse_options)

    try:
        trio.run(pyfuse3.main)

    except:
        pyfuse3.close(unmount=False)

        raise

    pyfuse3.close()


#

import sys

from archivecache import database, filesystem


mount_point = sys.argv[1]


database.init()


filesystem.mount_fs(mount_point)


#

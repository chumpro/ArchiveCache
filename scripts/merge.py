import sys

from archivecache import tabletree, database

path_old = sys.argv[1]
path_new = sys.argv[2]

database.init()

root = tabletree.Component()

directory_old = root.get(path_old)
directory_new = root.get(path_new)

directory_old.merge(directory_new)


#

import pathlib
import sys


from archivecache import tabletree, database


directory_path = sys.argv[1]

value = None

if len(sys.argv) > 2:
    value = sys.argv[2]

database.init()

directory = tabletree.Component().get(directory_path, create=True)

directory.set_value(value)


#

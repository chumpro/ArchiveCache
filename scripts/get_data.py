import pathlib
import sys


from archivecache import tabletree, database, version


version.require(0, 0)


if len(sys.argv) > 1:
    directory_path = sys.argv[1]

else:
    directory_path = ""


database.init()

directory = tabletree.Component().get(directory_path)

if directory is not None:
    print(directory.get_data())

# TODO: Return JSON

#

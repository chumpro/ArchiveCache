import pathlib
import sys


from archivecache import tabletree, database


source_path = sys.argv[1]
target_path = sys.argv[2]

database.init()

root = tabletree.Component()

source = root.get(source_path)

target = root.get(target_path, create=True)

target.set(source.get_data())


#

import pathlib
import sys


from archivecache import tabletree, database


directory_path = sys.argv[1]

database.init()

directory = tabletree.Component().get(directory_path)

directory.download()


#

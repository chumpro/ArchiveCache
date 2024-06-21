import sys

from archivecache import tabletree, database, cache


directory_path = sys.argv[1]

database.init()


print("info:", tabletree.Component().get(directory_path).info())

import sys

from archivecache import tabletree, database


directory_path = sys.argv[1]

database.init()


root = tabletree.Component()

directory = root.get(directory_path)


result = directory.verify_signature()

if result:
    print("OK")

else:
    print("FAIL")


#

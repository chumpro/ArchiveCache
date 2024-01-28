import sys
import json

from archivecache import tabletree, database


directory_path = sys.argv[1]

database.init()

root = tabletree.Component()

directory = root.get(directory_path)

directory.sign()

print(
    "Signed [%s] with signature [%s]."
    % (directory_path, directory.get_data_at(".signature"))
)


#

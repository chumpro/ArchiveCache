import sys

from archivecache import tabletree, database


value = sys.argv[1]


database.init()


ids = database.list_ids_of_value(value)

for id in ids:
    component = tabletree.Component(id)

    print("/".join(component.get_path()))


#

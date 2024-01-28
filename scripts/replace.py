import sys

from archivecache import tabletree, database


value = sys.argv[1]
replace_value = sys.argv[2]


database.init()


ids = database.list_ids_of_value(value)

for id in ids:
    component = tabletree.Component(id)

    component.set(replace_value)

    print("/".join(component.get_path()))


#

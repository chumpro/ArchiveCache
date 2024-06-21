import sys

from archivecache import tabletree, database


database.init()


root = tabletree.Component()

directory_root = root.get("root")
directory_nodes = root.get("nodes")


for key in directory_nodes.get_keys():
    component = directory_nodes.get(key).get("root")

    directory_root.merge(component)

    # TODO: Mark node as merged or remove it.
    # directory_nodes.get( key ).delete()


#

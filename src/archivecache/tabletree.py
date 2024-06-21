import base64
import json
import pyfuse3

from archivecache import database


def path_to_list(path):
    if type(path) == str:
        return [x for x in path.split("/") if x != ""]

    if type(path) in [list, tuple]:
        return [p1 for l1 in [path_to_list(p) for p in path] for p1 in l1]

    raise Exception("TableTree: path ", path, " was not string, list or tuple")


def Component(node_id=1):
    base = TableTree(node_id)

    if not base.exists():
        return base

    from archivecache import config_addons

    for addon in config_addons.addons:
        if hasattr(addon, "new"):
            component = addon.new(base)

            if component:
                return component

    return base


class TableTree(object):
    def __init__(self, node_id=1):
        self.node_id = node_id

        self.exists_flag = True

        self.update()

    def info(self):
        return str(self)

    def invalidate(self):
        self.exists_flag = False

    def exists(self):
        return self.exists_flag

    def update(self):
        result = database.get_record(self.node_id)

        if result is None:
            self.invalidate()

        else:
            self.parent_id, self.key, self.value = result

    def get_key(self):
        return self.key

    def get_keys(self):
        return database.get_keys(self.node_id)

    def get_id(self):
        return self.node_id

    def get_ids(self):
        return database.get_subids(self.node_id)

    def get_nodes(self):
        return [Component(node_id) for node_id in self.get_ids()]

    def get_parent(self):
        return Component(self.parent_id)

    def get_path(self):
        if self.key is None:
            return []

        return TableTree(self.parent_id).get_path() + [self.key]

    def get_value(self):
        return self.value

    def get(self, *path, create=False):
        path = path_to_list(path)

        if len(path) == 0:
            return self

        subid = database.get_id_at(self.node_id, path[0])

        if subid is None:
            if not create:
                return None

            subid = database.create_attribute(self.node_id, path[0])

        component = Component(subid)

        return component.get(path[1:], create=create)

    def get_data(self):
        if self.value is None:
            return {n.get_key(): n.get_data() for n in self.get_nodes()}

        else:
            return self.get_value()

    def get_data_at(self, key, default=None):
        node = self.get(key)

        if node is None:
            return default

        value = node.get_value()

        if value is None:
            struct = {n.get_key(): TableTree(n.get_id()) for n in node.get_nodes()}

            return struct

        return value

    def set_value(self, value=None):
        database.set_value(self.node_id, value)

        self.update()

    def set(self, value=None):
        if type(value) == dict:
            self.set_attributes(value)

        else:
            self.set_value(value)

        return self

    def set_attributes(self, attributes={}):
        for key, value in attributes.items():
            self.get(key, create=True).set(value)

    def delete(self):
        self.clear()

        database.delete_attribute(self.node_id)

        self.update()

    def clear(self):
        for node_id in self.get_ids():
            TableTree(node_id).delete()

        return self

    def get_layer(self):
        value = self.get_value()

        if value is not None:
            return value

        result = {}

        for node in self.get_nodes():
            result[node.get_key()] = node.get_value()

        return result

    def rebrand(self):
        return Component(self.node_id)

    def rehash(self):
        pass

    def upload(self):
        self.upload_nodes()

    def download(self):
        pass

    def upload_nodes(self):
        for node in self.get_nodes():
            node.upload()

    def get_content(self):
        pass

    def set_content(self, mapping):
        pass

    def get_reference(self):
        pass

    def fs_is_directory(self):
        pass

    def fs_readdir(self):
        pass

    def fs_data_size(self):
        pass

    def fs_open(self):
        pass

    def fs_read(self):
        pass

    def fs_write(self):
        pass

    def fs_attributes(self):
        pass

    def fs_unlink(self, fh):
        pass

    def fs_mkdir(self, key, mode, ctx):
        pass

    def merge(self, node):
        pass


#

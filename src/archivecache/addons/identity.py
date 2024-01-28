import base64
import json

from archivecache.addons import remote_directory
from archivecache import database, tabletree, version


version.require(0, 0)


def new(base):
    profile = base.get(".policy")

    if profile and profile.get_value() == "identity_v0":
        return AddonComponent(base.node_id)


class AddonComponent(remote_directory.AddonComponent):
    def get_content(self):
        return {
            n.get_key(): n.get_reference()
            for n in self.get_nodes()
            if n.get_key()
            not in [".ipfs_hash", ".cache", ".signature", ".owner", ".private_sign_key"]
        }


#

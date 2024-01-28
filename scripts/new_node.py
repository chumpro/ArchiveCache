import sys

from Crypto.PublicKey import RSA

from archivecache import tabletree, database, cache


directory_path = sys.argv[1]
owner_path = sys.argv[2]
#ip_address, ip_port = sys.argv[3].split(":")


database.init()

root = tabletree.Component()

directory = root.get(directory_path, create=True)

identity = root.get(owner_path)

ipfs_hash = identity.get_hash()

directory.clear().set(
    {
        ".policy": "remote_directory_v0",
#        ".ip_address": ip_address,
#        ".ip_port": ip_port,
        ".owner": ipfs_hash,
    }
)

node = directory.rebrand()

node.sign()

print("New identity at [%s] created with hash [%s]. " % (directory_path, ipfs_hash))


#

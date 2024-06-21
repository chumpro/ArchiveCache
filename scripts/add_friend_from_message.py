import sys

from archivecache import tabletree, database, packet


database.init()

root = tabletree.Component()


message = sys.stdin.buffer.read()

data = packet.message_to_data(message)


ipfs_hash = data[".ipfs_hash"]

if data[".policy"] == "identity_v0":
    if data[".ipfs_hash"] == data[".owner"]:
        root.get("friends", ipfs_hash, create=True).set(data)

        print("Added friend [%s]." % ipfs_hash)


#

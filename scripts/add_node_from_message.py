import sys

from archivecache import tabletree, database, packet, cache


database.init()

root = tabletree.Component()


message = sys.stdin.buffer.read()

data = packet.message_to_data(message)

temporary = cache.new_temporary().set(data).rebrand()

signature_ok = temporary.verify_signature()

ipfs_hash = temporary.get_data_at(".owner")

if signature_ok:
    root.get("nodes", ipfs_hash, create=True).set(temporary.get_data())

    print("Added node [%s]." % ipfs_hash)


temporary.delete()


#

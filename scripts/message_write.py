import sys

from archivecache import tabletree, database, packet


directory_path = sys.argv[1]

database.init()

root = tabletree.Component()

directory = root.get(directory_path, create=True)

message = sys.stdin.buffer.read()

data = packet.message_to_data(message)

directory.set(data)


#

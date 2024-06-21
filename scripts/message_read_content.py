import sys

from archivecache import tabletree, database, packet


directory_path = sys.argv[1]

database.init()

root = tabletree.Component()

directory = root.get(directory_path)

data = directory.get_content()

message = packet.data_to_message(data)

sys.stdout.buffer.write(message)


#

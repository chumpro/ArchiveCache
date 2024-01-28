import sys
import socket

from archivecache import tabletree, database, packet


node_path = sys.argv[1]
directory_path = sys.argv[2]

database.init()

root = tabletree.Component()

node = root.get(node_path)
directory = root.get(directory_path)

ip_address = node.get_data_at(".ip_address")
ip_port = node.get_data_at(".ip_port")

data = directory.get_reference()
message = packet.data_to_message(data)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((ip_address, int(ip_port)))

s.sendall(message.encode("utf-8"))

s.close()


#

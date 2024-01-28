import sys
import socketserver

from archivecache import tabletree, database, cache, packet


directory_path = sys.argv[1]

database.init()

root = tabletree.Component()

directory = root.get(directory_path)


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        message = b""

        while True:
            r = self.request.recv(1024)

            if not r:
                break

            message += r

        data = packet.message_to_data(message)

        temporary_key = cache.new_key()

        temporary = (
            root.get("temporary", temporary_key, create=True).set(data).rebrand()
        )  # .decrypt( identity )

        if temporary.verify_signature():
            owner_ipfs_hash = temporary.get_data_at(".owner")

            node = directory.get(owner_ipfs_hash, create=True).clear()

            node.set(temporary.get_data())

            print("Added new node from [%s]. " % owner_ipfs_hash)

        temporary.delete()

        self.request.sendall("FINE".encode())


socketserver.TCPServer.allow_reuse_address = True


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()


#

import sys
import json
import zlib

from archivecache import packet


json_text = sys.stdin.read()

message = packet.json_to_message(json_text)

sys.stdout.buffer.write(message)


#

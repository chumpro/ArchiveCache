import sys
import json
import zlib

from archivecache import packet


message = sys.stdin.buffer.read()

json_text = packet.message_to_json(message)

sys.stdout.write(json_text)


#

import zlib
import json
import base64


def data_to_message(data):
    json_string = json.dumps(data)

    message = json_to_message(json_string)

    return message


def message_to_data(message):
    json_string = message_to_json(message)

    data = json.loads(json_string)

    return data


def message_to_string(message):
    string = base64.b64encode(message)

    return message


def string_to_message(string):
    message = base64.b64decode(string)

    return message


def message_to_json(message):
    json_string = zlib.decompress(message).decode()

    return json_string


def json_to_message(json_string):
    message = zlib.compress(json_string.encode())

    return message


#

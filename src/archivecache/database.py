import sqlite3
import pathlib
import contextlib

from archivecache import tabletree, config


path = None
connection = None


def init(db_path=None):
    if db_path is None:
        db_path = config.db_path

    global path, connection

    if connection is None:
        connection = sqlite3.connect(db_path)

    return connection


def create(db_path):
    init(db_path)

    with connection:
        connection.execute(
            "CREATE TABLE attributes( id INTEGER PRIMARY KEY AUTOINCREMENT, container_id INTEGER, key TEXT, value, UNIQUE( container_id, key ) ON CONFLICT FAIL )"
        )

        connection.execute(
            "INSERT INTO attributes VALUES ( NULL, ?, ?, ? )", [0, None, None]
        )


def get_record(node_id):
    with connection:
        result = list(
            connection.execute(
                "SELECT container_id, key, value FROM attributes WHERE id = ?",
                [node_id],
            )
        )

        if len(result) == 1:
            return result[0]

        else:
            return None


def get_value(node_id):
    with connection:
        result = list(
            connection.execute("SELECT value FROM attributes WHERE id = ?", [node_id])
        )

        if len(result) == 1:
            return result[0][0]

        else:
            return None


def get_subids(node_id):
    with connection:
        result = list(
            connection.execute(
                "SELECT id, key, value FROM attributes WHERE container_id = ?",
                [node_id],
            )
        )

        return [r[0] for r in result]


def get_id_at(node_id, key):
    with connection:
        result = list(
            connection.execute(
                "SELECT id FROM attributes WHERE container_id = ? AND key = ?",
                [node_id, key],
            )
        )

        if len(result) == 1:
            return result[0][0]

        return None


def get_keys(node_id):
    with connection:
        result = list(
            connection.execute(
                "SELECT key FROM attributes WHERE container_id = ?", [node_id]
            )
        )

        return [r[0] for r in result]


# NOTE: create_attribute does not remove duplicate keys!
def create_attribute(node_id, key, value=None):
    with contextlib.closing(connection.cursor()) as cursor:
        result = list(
            cursor.execute(
                "INSERT INTO attributes VALUES ( NULL, ?, ?, ? )", [node_id, key, value]
            )
        )

        result = cursor.lastrowid

        return result


def set_value(node_id, value):
    with connection:
        result = list(
            connection.execute(
                "UPDATE attributes SET value = ? WHERE id = ?", [value, node_id]
            )
        )


def delete_attribute(node_id):
    with connection:
        result = list(
            connection.execute("DELETE FROM attributes WHERE id = ?", [node_id])
        )


def list_ids_of_value(value):
    with connection:
        result = list(
            connection.execute("SELECT id FROM attributes WHERE value = ?", [value])
        )

        return [r[0] for r in result]


#

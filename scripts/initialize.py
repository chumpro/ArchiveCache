import pathlib
import sys


from archivecache import tabletree, database, config


db_path = config.db_path


if pathlib.Path(db_path).exists():
    print(
        "Database at", db_path, "allready exists. Delete it and then create a new one."
    )

else:
    database.create(db_path)

    database.init()

    print("Creating new database at", db_path, ".")

    component = tabletree.Component()

    component.set(
        {
            "root": {
                "forum": {
                    ".policy": "remote_directory_v0",
                },
                "projects": {
                    ".policy": "remote_directory_v0",
                },
            },
        }
    )


#

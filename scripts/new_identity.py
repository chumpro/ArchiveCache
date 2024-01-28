import sys

from Crypto.PublicKey import RSA

from archivecache import tabletree, database, cache


directory_path = sys.argv[1]

database.init()

root = tabletree.Component()


key = RSA.generate(2048)


directory = root.get(directory_path, create=True)

directory.clear()

directory.set(
    {
        ".policy": "identity_v0",
        ".private_sign_key": key.export_key().decode(),
        ".public_signature_verification_key": key.publickey().export_key().decode(),
    }
)


identity = directory.rebrand()


ipfs_hash = identity.get_hash()


identity.set({".owner": ipfs_hash})


friend = root.get("friends", ipfs_hash, create=True)

friend.set(identity.get_data())

identity.sign()

print("New identity at [%s] created with hash [%s]. " % (directory_path, ipfs_hash))


#

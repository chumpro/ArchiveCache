import os
import stat
import json
import base64

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import pyfuse3


from archivecache import database, tabletree, ipfs, cache, version, packet


version.require(0, 0)


# NOTE: For encryption, use document hash as key.


class AddonComponent(tabletree.TableTree):
    def fs_unlink(self, key):
        component = self.get(key)

        if component is not None:
            component.delete()

            self.rehash()

            return True

        return False

    def read_json_directory_from_ipfs(self, ipfs_hash):
        cache_key = ipfs.copy_to_cache(ipfs_hash)

        with open(cache.full_file_path(cache_key)) as f:
            json_directory_description = f.read()

            self.get(".cache", create=True).set(cache_key)

            return json_directory_description

    def get_hash(self):
        self.upload()

        return self.get_data_at(".ipfs_hash")

    def rehash(self):
        ipfs_hash_old = None

        ipfs_hash_component = self.get(".ipfs_hash")

        if ipfs_hash_component is not None:
            ipfs_hash_old = ipfs_hash_component.get_value()

            ipfs_hash_component.delete()

        self.upload()

        ipfs_hash_new = self.get_data_at(".ipfs_hash")

        if ipfs_hash_old != ipfs_hash_new:
            self.sign()

            self.get_parent().rehash()

    def get_signature_content(self):
        self.upload()

        return {
            n.get_key(): n.get_reference()
            for n in self.get_nodes()
            if n.get_key() in [".policy", ".ipfs_hash"]
        }

    def is_local_owned(self):
        owner_hash = self.get(".owner")

        if owner_hash is not None:
            owner_identity = tabletree.Component().get("friends", owner_hash)

            if owner_identity is not None:
                private_sign_key = owner_identity.get(".private_sign_key")

                if private_sign_key is not None:
                    return True

        return False

    def sign(self):
        self.upload()

        identity_hash = self.get_data_at(".owner")

        if identity_hash is not None:
            identity = tabletree.Component().get("friends", identity_hash)

            if identity is not None:
                key_text = identity.get_data_at(".private_sign_key")

                if key_text is not None:
                    private_key = RSA.import_key(key_text)

                    message = packet.data_to_message(self.get_signature_content())

                    h = SHA256.new(message)

                    signature = pkcs1_15.new(private_key).sign(h)

                    owner_hash = identity.get_hash()

                    self.set(
                        {
                            ".owner": owner_hash,  # TODO: Do not set owner here!
                            ".signature": base64.b64encode(signature).decode("utf-8"),
                        }
                    )

                    # TODO: self.rehash()

    # TODO : sort data before signing.

    # TODO : use own.py to set the owner.

    def verify_signature(self):
        identity_hash = self.get_data_at(".owner")

        if identity_hash is not None:
            identity = tabletree.Component().get("friends", identity_hash)

            if identity is not None:
                key_text = identity.get_data_at(".public_signature_verification_key")

                if key_text is not None:
                    public_key = RSA.importKey(key_text)

                    message = packet.data_to_message(self.get_signature_content())

                    signature_text = self.get_data_at(".signature")

                    if signature_text is not None:
                        signature = base64.b64decode(signature_text.encode("utf-8"))

                        h = SHA256.new(message)

                        try:
                            pkcs1_15.new(public_key).verify(h, signature)

                        except ValueError:
                            return False

                        return True

        return False


#

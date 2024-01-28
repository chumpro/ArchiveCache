

                ArchiveCache

ArchiveCache is a simple, extensible, decentialized filesystem. Users can create their own folders, share data and discuss. There is no central servers. ArchiveCache currently uses IPFS, but can be extended to use other similar types of tech.


        Installation

Warning: This software is in its early testing fase. A current known attack is flooding, but there can be all kinds of security issues. When using ArchiveCache limit communitation to people you trust and use a virtual machine. Do not put anything important on ArchiveCache and keep backups whenever you do.

Requirements: I use python 10 with pip. This has been tested with multiple docker containers on a docker network. The docker image was based on ubuntu.


    Install IPFS

Follow instructions to install IPFS kubo, I used v0.26.0, from here: https://github.com/ipfs/ipfs-docs/blob/main/docs/install/command-line.md


    Install python ( for apt )

> sudo apt install python3 python3-pip


    Install pyfuse3

> sudo apt install python3-pyfuse3

    Install cryptodome

> pip install pycryptodome

    Install ArchiveCache

> git pull https://github.com/chumpro/ArchiveCache.git

> cd ArchiveCache

> pip install -e .



    Initialize IPFS ( if neccesary )

> ipfs init
    
    and start IPFS

> ipfs daemon &




    Setting up your node


ArchiveCache uses a tree structured database to model the filesystem. The commands in the scripts folder uses paths into the datastructure. These are similar to filesystem paths but they are not identical. To actually mount the filesystem work your way to the end of these instructions.


Edit the src/ArchiveCache/config.py to set the location of the database file.

Make room for cached files:

> mkdir cache


Initialize an empty database.

> python3 scripts/initialize.py


Create an identity. This identity will be used as the owner of the node. You can have other identities for messages and content.

> python3 scripts/new_identity.py identities/YOURNAMEHERE


To verify that the identity is set up correctly and signed:

> python3 scripts/verify.py identities/YOURNAMEHERE

This should say 'OK'.


To create a new node:

> python3 scripts/new_node.py node identities/YOURNAMEHERE

Verify that everything is ok so far:

> python3 scripts/verify.py node


ArchiveCache uses "messages". A message is compressed JSON. In order to send and recieve messages manually, like over e-mail, a message is encoded in base64.
There are scripts for this.


To get message constituting a reference to your identity as base64:

> python3 scripts/message_read_reference.py identities/YOURNAMEHERE | base64 --wrap=0

The data should be sent to your friends to set up communications.


When you receive a base64 message with an identity, you can add this to your friends list:

> echo BASE64ENCODEDMESSAGE | base64 --decode | python3 scripts/add_friend_from_message.py


To look at the message first write:

> echo BASE64ENCODEDMESSAGE | base64 --decode | python3 scripts/message_to_json.py

The message should look something like this:

{".ipfs_hash": "SOME_IPFS_HASH", ".owner": "SAME_IPFS_HASH", ".policy": "identity_v0", ".signature": "DIGITAL_SIGNATURE"}


To send your node references to your friends, so that they can add your files to their nodes, you can do this manually too.

> python3 scripts/message_read_reference.py node | base64 --wrap=0

Gives you the base64 message to your current node, your ArchiveCache root. Send it with e-mail or similar.

To add friend nodes to your list of nodes:

> echo BASE64ENCODEDMESSAGE | base64 --decode | python3 scripts/add_node_from_message.py

This requires that the reference is signed by a friend.



The big, important part is still missing; merging the roots of your friends nodes in to your node's root.

> python3 scripts/merge.py root nodes/FRIEND_HASH/root


Now you have the files and directories that your friends have created and changed. Ownerships and other vessles of control applies. Only those directories that have policy remote_directory_v0 and no owner can be added to by all.


To merge all node roots:

> python3 scripts/merge_all.py

To remove the nodes that have been merged:

> python3 scripts/delete.py nodes




To wrap it all up rebuild your node:

> python3 scripts/new_node.py node identities/YOURNAMEHERE

Create the new base64 message:

> python3 scripts/message_read_reference.py node | base64 --wrap=0

And send it to your friends.



    Mounting the filesystem, FINALLY!


To mount the filesystem write:

> mkdir MOUNTPOINT

> python3 scripts/mount.py MOUNTPOINT &

Running scripts while the filesystem is mounted, can yield inconsistencies in the filesystem. This will be fixed in the future. It involves packaging everything in the same process.




    Automation.

It is possible to automate this process. I have avoided automation in order to make this significantly easier to understand and debug. Also, there are many different ways to automate.
Some simple facilities exists.

To listen for incoming node references from friends:

> python3 scripts/receive.py nodes

To send a node reference to a friend:

> python3 scripts/send.py nodes/FRIEND_HASH node



        Suggestions

Feel free to give suggestion. I will focus on bug fixing and security hardening. There will be automatic sharing of data and discovery of new friends later.



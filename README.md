
# ArchiveCache

ArchiveCache is a simple, extensible, decentralized filesystem. Users can create their own folders, share data and discuss. There is no central servers. ArchiveCache currently uses IPFS, but can be extended to use other similar types of tech.

ArchiveCache is not an application. It is a framework and a set of tools to use it. It is written in Python, but there are shell command that can be used in scripting. There are just too many ways to use ArchiveCache for it to be a point and click application.

ArchiveCache can be used to collaboratively manage large decentralized directory structures. One can use it as a source control system, to share large datasets or any kind of information that sits in directories. Since IPFS handles large files, ArchiveCache can be used to share nn checkpoints as well as docker images or similar. One can also use it for websites and even directly share live runtime environments such as python venv or conda. Package repositories can also be efficiently share on ArchiveCache. ArchiveCache opens up new new ways to collaborate.

Due to how ArchiveCache references data it can be used with other networking systems besides IPFS, such as HTTP, FTP, magnet links, Freenode, TCP/IP directly or anything else you can come up with. There are simply no limitations built in to ArchiveCache. 

The best part about ArchiveCache is that it is very simple and straight forward.

ArchiveCache filesystem works like this:

- Each user has a local version of the filesystem.
- Users can freely edit their filesystem.
- Data is stored on IPFS.
- Users share a link to the root of their filesystem ( an IPFS CID ).
- Users **merge** other users filesystems into their own ( rules such as ownership with signatures apply here ).
- The modifying - merging - sharing cycle is what causes information propagates through the network. 

## Installation

Warning: This software is in its early testing phase. There can be security issues. When using ArchiveCache limit communication to people you trust and use a virtual machine. Do not put anything important on ArchiveCache and keep backups whenever you do.

Requirements: I use python 3.10. This has been tested with multiple docker containers on a docker network. The docker image was based on Ubuntu.

These instructions apply to people who use apt. Consider creating a python environment or use conda.

### Install IPFS

Follow instructions to install IPFS kubo, I used v0.26.0, from here: https://github.com/ipfs/ipfs-docs/blob/main/docs/install/command-line.md.
Make sure IPFS is initialized and started.

### Install python

    sudo apt install python3 python3-pip

### Install pyfuse3

    sudo apt install python3-pyfuse3

### Install cryptodome

    pip install pycryptodome

### Install ArchiveCache

    git pull https://github.com/chumpro/ArchiveCache.git
    cd ArchiveCache
    pip install -e .

### Setting up your node

ArchiveCache uses a tree structured database to model the filesystem. The commands in the scripts folder uses paths into the data structure. These are similar to filesystem paths but they are not identical. To actually mount the filesystem work your way to the end of these instructions.

Edit the src/ArchiveCache/config.py to set the location of the database file.

Make room for cached files:

    mkdir cache

Initialize an empty database.

    python3 scripts/initialize.py

Create an identity. This identity will be used as the owner of the node.

    python3 scripts/new_identity.py identities/YOURNAMEHERE

To verify that the identity is set up correctly and signed:

    python3 scripts/verify.py identities/YOURNAMEHERE

This should say 'OK'.

To create a new node:

    python3 scripts/new_node.py node identities/YOURNAMEHERE

Verify that everything is OK so far:

    python3 scripts/verify.py node

ArchiveCache uses "messages". A message is compressed JSON. In order to send and receive messages manually, like over e-mail, a message is encoded in base64.

To get message constituting a reference to your identity as base64:

    python3 scripts/message_read_reference.py identities/YOURNAMEHERE | base64 --wrap=0

The data should be sent to your friends to set up communications.

When you receive a base64 message with an identity, you can add this to your friends list:

    echo BASE64ENCODEDMESSAGE | base64 --decode | python3 scripts/add_friend_from_message.py

To look at the message first write:

    echo BASE64ENCODEDMESSAGE | base64 --decode | python3 scripts/message_to_json.py

The message should look something like this:

    {".ipfs_hash": "SOME_IPFS_HASH", ".owner": "SAME_IPFS_HASH", ".policy": "identity_v0", ".signature": "DIGITAL_SIGNATURE"}

To send your node references to your friends, so that they can add your files to their nodes, you can do this manually too.

    python3 scripts/message_read_reference.py node | base64 --wrap=0

Gives you the base64 message to your current node, your ArchiveCache root. Send it with e-mail or similar.

To add friend nodes to your list of nodes:

    echo BASE64ENCODEDMESSAGE | base64 --decode | python3 scripts/add_node_from_message.py

This requires that the reference is signed by a friend.

The big, important part is still missing; merging the roots of your friends nodes in to your node's root.

    python3 scripts/merge.py root nodes/FRIEND_HASH/root

Now you have the files and directories that your friends have created and changed. Only those directories that have policy remote_directory_v0 and no owner can be added to by all.

To merge all node roots:

    python3 scripts/merge_all.py

To remove the nodes that have been just been merged:

    python3 scripts/delete.py nodes

To wrap it all up rebuild your node:

    python3 scripts/new_node.py node identities/YOURNAMEHERE

Create the new base64 message:

    python3 scripts/message_read_reference.py node | base64 --wrap=0

And send it to your friends.

### Mounting the filesystem

To mount the filesystem write:

    mkdir MOUNTPOINT
    python3 scripts/mount.py MOUNTPOINT &

Running scripts while the filesystem is mounted, can yield inconsistencies in the filesystem. This will be fixed in the future. It involves packaging everything in the same process.

### Automation

It is possible to automate this process. I have avoided automation in order to make this easier to understand and debug and safer to test. Also, there are many different ways to automate. Some simple facilities exists.

To listen for incoming node references from friends:

    python3 scripts/receive.py nodes

To send a node reference to a friend:

    python3 scripts/send.py nodes/FRIEND_HASH node

## Contributions

Feel free to give contribute and give suggestion. I will focus on bug fixing and security hardening. There will be automatic sharing of data and discovery of new friends later.

Monero: 48hRRk1mN9nVLVrUL8e7qLNznEXzvsXzqWW24jurw4QAcaTwUa1K9FwGkzwkfGFNSzL58zNPLEGBeet6ELJ5VZ4zKDjdqiP



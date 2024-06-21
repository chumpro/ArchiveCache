current_branch = "original"

current_version = [
    0,  # This number increases by one whenever backwards compatibility is broken.
    0,  # This number increases by one whenever a feature is added or a bug is fixed.
]


def check(*required_version, required_branch=current_branch):
    if current_branch != required_branch:
        return False

    if current_version[0] != required_version[0]:
        return False

    if current_version[1] < required_version[1]:
        return False

    return True


def require(*required_version, required_branch=current_branch, message=""):
    if not check(*required_version, required_branch=required_branch):
        raise Exception(
            "An ArchiveCache addon is probably incompatible with your version of ArchiveCache. Current",
            to_string(current_version),
            "Required",
            to_string(required_version),
            message,
        )


def to_string(v, branch=current_branch):
    return "%s-v%d.%d" % [branch] + v


#

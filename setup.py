import setuptools


packages = setuptools.find_packages(where="src")

print("setup packages", packages)

setuptools.setup(
    name="ArchiveCache",
    version="0.0.1",
    install_requires=[],
    # scripts = [
    #     'scripts/archivecache-mount',
    #     'scripts/archivecache-directory-sign',
    #     'scripts/archivecache-identity-create',
    #     'scripts/archivecache-database-clean',
    #     'scripts/archivecache-database-init',
    #     'scripts/archivecache-mount',
    # ],
    package_dir={"": "src"},
    packages=packages,
    #    py_modules = [],
    # entry_points = {
    #     'console_scripts' : [
    #         'archivecache-mount = archivecache.fs:mount',
    #     ]
    # }
)


#

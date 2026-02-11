import os
import argparse
import ast
import re
import glob

# the fields that should always be the same
DEFAULT_DATA = {
    "author": "QOC Innovations",
    "website": "qocinnovations.com",
    "license": "OPL-1",
}


def check_manifest(file, data):
    # output any issues with some manifest that needs manual intervention
    version_parse = re.compile(r"\d+\.0\.\d+.\d+.\d+")
    version = data.get("version", False)
    if not version:
        print(f"{file} has no version")
    if not version_parse.match(version):
        print(
            f"{file}'s version {version} doesn't match <odoo version>.0.<major>.<minor>.<patch>"
        )


def fix_manifest(file):
    d = None
    with open(file, "r") as f:
        data = f.read()
        d = ast.literal_eval(data)
    if not isinstance(d, dict):
        print(f"{file} is not readable as a python dictionary")
        return
    d.update(DEFAULT_DATA)
    check_manifest(file, d)
    with open(file, "w") as f:
        f.write(str(d))


def apply_to_manifests(dir, func):
    for root, _, files in os.walk(dir):
        for file in files:
            if file == "__manifest__.py":
                func(os.path.join(root, file))


def walk_globs(glob_dirs):
    for glob_dir in glob_dirs:
        full_path = os.path.expanduser(glob_dir)
        dirs = glob.glob(full_path)
        for dir in dirs:
            apply_to_manifests(dir, fix_manifest)


def main():
    parser = argparse.ArgumentParser(description="Check and fix manifest files")
    parser.add_argument(
        "dirs",
        nargs="+",
        help="The directory (can be a glob pattern) to look for manifest files in",
    )
    args = parser.parse_args()
    glob_dirs = args.dirs
    walk_globs(glob_dirs)


if __name__ == "__main__":
    main()

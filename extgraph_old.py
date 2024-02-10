# first version of the extgraph.py that isnt object oriented, only -r, -h, -v are working.

import os
import sys
import json

def is_file(path):
    try:
        return not os.stat(path)[0] & 0x4000
    except FileNotFoundError:
        return False

def is_path_exists(path):
    try:
        return os.stat(path)[0] & 0x4000
    except FileNotFoundError:
        return False

# (required) check if path is given and exists
try:
    path = sys.argv[1]
    if not is_path_exists(path):
        print(f"the path specified '{path}' does not exist.")
        sys.exit(1)
except IndexError:
    path = os.getcwd()

# check if a argument is passed
graph = False
recursive = False
buffer = False
remove_arg = []

try:
    args = sys.argv[2:]
    for arg in args:
        if not arg.startswith(("-", "--")):
            pass

        elif arg in ["-g", "--graph"]:
            graph = True
            remove_arg.append(arg)
        elif arg in ["-r", "--recursive"]:
            recursive = True
            remove_arg.append(arg)
        elif arg in ["-b", "--buffer"]:
            buffer = True
            remove_arg.append(arg)
        elif arg in ["-h", "--help"]:
            print("Usage: extgraph.py <path> [-g] [-r] [-h] [extension1 .extension2 ...]")
            remove_arg.append(arg)
            # exit?
        elif arg in ["-v", "--version"]:
            print("extgraph.py v0.0.1")
            remove_arg.append(arg)
            # exit?
        else:
            print(f"Invalid argument: {arg}")
            sys.exit(1)
    args = [arg for arg in args if arg not in remove_arg]
except IndexError:
    pass

# recursive here
# ...

if buffer:
    with open("buffer.json", "r") as f:
        load_buffer = json.load(f)

    for key, value in load_buffer.items():
        print(f"{key}: {value}")
    sys.exit(0)


file_1 = []
folder_1 = []
PermissionError_files = []
FileNotFoundError_files = []
OSError_files = []
def recursive_search(path):
    """
    Recursively removes the specified directory. Based on Roberthh's implementation: https://forum.micropython.org/viewtopic.php?t=7512#p42783.
    """
    if is_path_exists(path):
        try:
            for item in os.listdir(path):
                try:
                    if is_file(f"{path}/{item}"):
                        file_1.append(item)
                    else:
                        folder_1.append(item)
                    recursive_search(f"{path}/{item}")
                except OSError:
                    OSError_files.append(path.split("/")[-1])
        except FileNotFoundError:
            FileNotFoundError_files.append(path.split("/")[-1])
        except PermissionError:
            PermissionError_files.append(path.split("/")[-1])

if recursive:
    recursive_search(path)
    files = file_1
    folders = folder_1
    # print(f"PermissionError: {PermissionError_files}")
    # print(f"FileNotFoundError: {FileNotFoundError_files}")
    # print(f"OSError: {OSError_files}")

else:
    files = [f for f in os.listdir(path) if is_file(f"{path}/{f}")]
    folders = [d for d in os.listdir(path) if not is_file(f"{path}/{d}")]

filewithext = []
filewithoutext = []
filehidden = []

# filter files with and without extension
for file in files:
    if file.startswith("."):
        filehidden.append(file)
        continue
    split_file = file.split(".")
    if len(split_file) == 2:
        filewithext.append(file)
    else:
        filewithoutext.append(file)

# create a dictionary with the extentions as keys
extentions = {ext: [] for ext in args}
extentions["files"] = []
extentions["folders"] = []
extentions["others"] = []

listofext = list(extentions.keys())

# filter files to its corresponding extension
for file in filewithext:
    file_ext = f".{file.split(".")[-1]}"

    if file_ext in listofext:
        extentions[file_ext].append(file)
    else:
        # if the extension is not specified by the user, it will be in the "others" key
        extentions["others"].append(file)

# add other stuffs to its corresponding key
extentions["files"] = filewithext
extentions["others"] += filewithoutext + filehidden
extentions["folders"] = folders

# graph here
# ...
# else
# display raw data

with open("buffer.json", "w") as f:
    f.write(json.dumps(extentions))

for key, value in extentions.items():
    print(f"{key}: {value}")
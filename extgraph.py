# this program is still on development, no graph and in-dept instructions to use or informations is created yet.
version = "v0.0.10"

import os
import sys
import json


class extgraph:
    def __init__(self) -> None:
        # self.graph = False
        self.number = False
        self.recursive = False
        self.buffer = False
        self.args = []
        self.path = []

    def display_help(self):
        print("Usage: extgraph.py <path> [-r] [-n] [extension1 .extension2 ...]")
        print("       extgraph.py [-b] [-n] [extension1 .extension2 ...]")
        print("       extgraph.py [-h] [-v]")
        print("       extgraph.py")

    def display_version(self):
        print(f"extgraph.py {version}")

    def is_file(self, path):
        try:
            return not os.stat(path)[0] & 0x4000
        except FileNotFoundError:
            return False

    def is_path_exists(self, path):
        try:
            return os.stat(path)[0] & 0x4000
        except FileNotFoundError:
            return False

    def recursive_search(self, path):
        """
        Recursively traverse the directory. Based on Roberthh's implementation: https://forum.micropython.org/viewtopic.php?t=7512#p42783.
        """
        values = {"files": [], "folders": [], "error_paths": []}

        if self.is_path_exists(path):
            try:
                for item in os.listdir(path):
                    try:
                        if self.is_file(f"{path}/{item}"):
                            values["files"].append(item)
                        else:
                            values["folders"].append(item)
                        recursive_values = self.recursive_search(f"{path}/{item}")
                        values = {key: values[key] + recursive_values[key] for key in values}
                    except OSError:
                        values["error_paths"].append(path)
            except (FileNotFoundError, PermissionError):
                values["error_paths"].append(path)
        return values

    def filter_by_extensions(self, files, folders, error_paths):
        """
        filter the files and folder to its respective extension and category.
        """
        filewithext = []
        filewithoutext = []
        filehidden = []

        for file in files:
            if file.startswith("."):
                filehidden.append(file)
                continue
            split_file = file.split(".")
            if len(split_file) == 2:
                filewithext.append(file)
            else:
                filewithoutext.append(file)

        extentions = {ext: [] for ext in self.args}
        extentions["files"] = []
        extentions["folders"] = []
        extentions["error_paths"] = []

        listofext = list(extentions.keys())

        for file in filewithext:
            file_ext = f".{file.split('.')[-1]}"

            if file_ext in listofext:
                extentions[file_ext].append(file)
            else:
                extentions["files"].append(file)
        
        extentions["files"] += filewithext + filewithoutext + filehidden
        extentions["folders"] += folders
        extentions["error_paths"] += error_paths

        return extentions

    def set_path(self, path):
        """
        set the path to work with, if the path doesnt exist, exit the program.
        """
        if not self.is_path_exists(path):
            print(f"the path specified '{path}' does not exist.")
            sys.exit(1)
        return path

    def save_buffer(self, dict):
        """
        save the dict in a json format.
        """
        with open("buffer.json", "w") as f:
            f.write(json.dumps(dict))

    def load_buffer(self):
        """
        load the previous saved json file and return the files and folders.
        this would throw "no buffer found" for the first time obviously, run the program first.
        """
        try:
            with open("buffer.json", "r") as f:
                load_buffer = json.load(f)
            return load_buffer["files"], load_buffer["folders"], load_buffer["error_paths"]
        except FileNotFoundError:
            print("no buffer found, run the program first without '-b or --buffer' flag")
            sys.exit(1)

    def read_data(self, dict):
        """
        read the dict.
        """
        for key, value in dict.items():
            if self.number:
                print(f"{key}: {len(value)}")
            else:
                print(f"{key}: {value}")

    def parse_args(self, args):
        """
        validate the flags in the input, then remove it to prevent it from being a file extension.
        """
        flags = ["-r", "--recursive", "-n", "--number", "-b", "--buffer", "-h", "--help", "-v", "--version"]
        to_remove = []
        
        for arg in args:
            if arg.startswith(("-", "--")) and not arg in flags:
                print(f"Invalid argument: {arg}")
                sys.exit(1)
        
        if "-h" in args or "--help" in args:
            self.display_help()
            sys.exit(0)

        if "-v" in args or "--version" in args:
            self.display_version()
            sys.exit(0)

        # buffer and recursion cannot be used at the same time.
        if ("-r" in args or "--recursive" in args) and ("-b" in args or "--buffer" in args):
            print("recursion and buffer cannot be used at the same time.")
            sys.exit(1)

        # if -b is used, ignore the path, and read the buffer.
        if "-b" in args or "--buffer" in args:
            if args[0] != "-b" and args[0] != "--buffer" and not args[0].startswith(("-", "--")):
                print(f"path {args[0]} is ignored when using -b flag, loading the buffer.json content instead.")
                to_remove.append(args[0])
            self.buffer = True
            to_remove += ["-b", "--buffer"]

        if "-n" in args or "--number" in args:
            # self.graph = True
            self.number = True
            to_remove += ["-n", "--number"]
        
        if "-r" in args or "--recursive" in args:
            print("recursion is enabled.")
            self.recursive = True
            to_remove += ["-r", "--recursive"]

        # initialize the path if its not in buffer mode, use the cwd when path index is a flag, otherwise, the specified one.
        if not self.buffer:
            if args[0] in flags:
                self.path = self.set_path(os.getcwd())
                to_remove.append(args[0])
            else:
                self.path = self.set_path(args[0])
                to_remove.append(args[0])

        return [arg for arg in args if arg not in to_remove]

    def run(self, args):
        """
        run the program.
        """
        # parse the arguments.
        self.args = self.parse_args(args)

        if self.buffer:
            files, folders, error_paths = self.load_buffer()
        elif self.recursive:
            values = self.recursive_search(self.path)
            files, folders, error_paths = values["files"], values["folders"], values["error_paths"]
        else:
            files = [f for f in os.listdir(self.path) if self.is_file(f"{self.path}/{f}")]
            folders = [d for d in os.listdir(self.path) if not self.is_file(f"{self.path}/{d}")]
            error_paths = [] # work on this later.

        extensions = self.filter_by_extensions(files, folders, error_paths)

        if not self.buffer:
            self.save_buffer(extensions)
        
        self.read_data(extensions)

try:
    ext = extgraph()
    ext.run(sys.argv[1:])
except IndexError:
    ext.run([os.getcwd()])
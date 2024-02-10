# this program is still on development, no graph and in-dept instructions to use or informations is created yet.
# but this already outputs the necessary stuffs. This is the initial commit.
# current version: v0.0.1

# known issue:
#   given <path> doesnt do anything when using -b, it only reads the buffer and exit the program. (FIXED)
#       > similar: should -h and -v ignore the rest of the args and print and exit only when they're on path location?
#       > similar: should -h and -v be executed together, or even the main program flags (-r, -g, -b) with it? (opinion)

import os
import sys
import json

class extgraph:
    def __init__(self, path=None, args=None) -> None:
        self.graph = False
        self.recursive = False
        self.buffer = False

        self.args = self.parse_args(args)
        
        if path:
            self.path = self.set_path(path)
        

    def display_help(self):
        print("Usage: extgraph.py <path> [-g] [-r] [-h] [-v] [extension1 .extension2 ...]")
        print("       extgraph.py -b [-g] [-h] [-v] [extension1 .extension2 ...]")

    def display_version(self):
        print("extgraph.py v0.0.1")

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
        values = {"files": [], "folders": [], "error_path": []}

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
                        values["error_path"].append(path)
            except (FileNotFoundError, PermissionError):
                values["error_path"].append(path)
        return values

    def filter_by_extensions(self, files, folders):
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
        extentions["others"] = []

        listofext = list(extentions.keys())

        for file in filewithext:
            file_ext = f".{file.split(".")[-1]}"

            if file_ext in listofext:
                extentions[file_ext].append(file)
            else:
                extentions["others"].append(file)
        
        extentions["files"] += filewithext + filewithoutext + filehidden
        extentions["folders"] += folders
        extentions["others"] += filewithoutext + filehidden

        return extentions

    def set_path(self, path):
        """
        set the path to work with, if the path doesnt exist, exit the program.
        """
        if not self.is_path_exists(path):
            print(f"the path specified '{path}' does not exist.")
            sys.exit(1)
        return path

    def parse_args(self, args):
        """
        validate the flags in the input, then remove it to prevent it being a file extension.
        """
        to_remove_arg = []
        try:
            # args = sys.argv[2:]
            for arg in args:
                if not arg.startswith(("-", "--")):
                    pass
                
                elif ("-r" in args or "--recursive" in args) and ("-b" in args or "--buffer" in args):
                    print("recursion and buffer cannot be used at the same time.")
                    sys.exit(1) 
                elif arg in ["-g", "--graph"]:
                    self.graph = True
                    to_remove_arg.append(arg)
                elif arg in ["-r", "--recursive"]:
                    self.recursive = True
                    to_remove_arg.append(arg)
                elif arg in ["-b", "--buffer"]:
                    self.buffer = True
                    to_remove_arg.append(arg)
                elif arg in ["-h", "--help"]:
                    self.display_help()
                    to_remove_arg.append(arg)
                elif arg in ["-v", "--version"]:
                    self.display_version()
                    to_remove_arg.append(arg)
                else:
                    print(f"Invalid argument: {arg}")
                    sys.exit(1)
        
            return [arg for arg in args if arg not in to_remove_arg]
        except IndexError:
            return args

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
            return load_buffer["files"], load_buffer["folders"]
        except FileNotFoundError:
            print("no buffer found, run the program first without '-b or --buffer' flag")
            sys.exit(1)

    def read_data(self, dict):
        """
        read the dict.
        """
        for key, value in dict.items():
            if key != "files":
                print(f"{key}: {value}")

    def run(self):
        """
        starting point of the extgraph class, used to execute things and stuffs.
        """
        if self.buffer:
            extensions = self.filter_by_extensions(*self.load_buffer()) # unpack the tuple returned by load_data()
            self.read_data(extensions)
            sys.exit(0)
        else:
            if self.recursive:
                result = self.recursive_search(self.path)
                files, folders = result["files"], result["folders"]
            else:
                files = [f for f in os.listdir(self.path) if self.is_file(f"{self.path}/{f}")]
                folders = [d for d in os.listdir(self.path) if not self.is_file(f"{self.path}/{d}")]

            extensions = self.filter_by_extensions(files, folders)
            self.save_buffer(extensions)
            self.read_data(extensions)

try:
    # ["-b", "--buffer", "-h", "--help", "-v", "--version"]:
    if "-b" in sys.argv or "--buffer" in sys.argv:
        if sys.argv[1] != "-b" and sys.argv[1] != "--buffer":
            print(f"note: path '{sys.argv[1]}' is ignored. no path is required, when using -b flag.")
            del sys.argv[1]
        ext = extgraph(args=sys.argv[1:])
    else:
        ext = extgraph(sys.argv[1], sys.argv[2:])
    ext.run()
except IndexError:
    print(f"expected a path after {sys.argv[0]}")
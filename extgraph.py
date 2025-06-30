import os
import sys
import json
import matplotlib.pyplot as plt


class extgraph:
    def __init__(self) -> None:
        self.graph = False
        self.number = False
        self.recursive = False
        self.buffer = False
        self.args = []
        self.path = []

    def display_help(self):
        print("Usage: extgraph.py <path> [-r] [-n | -g] [extension1 .extension2 ...]")
        print("       extgraph.py [-b] [-n | -g] [extension1 .extension2 ...]")
        print("       extgraph.py [-h]")
        print("       extgraph.py")

    def is_hidden(self, path):
        try:
            return os.stat(path).st_file_attributes & 0x02 != 0
        except FileNotFoundError:
            return False

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
        """recursively traverse the directory. Based on Roberthh's implementation: https://forum.micropython.org/viewtopic.php?t=7512#p42783."""
        items = {"files": [], "folders": [], "hidden": [], "error_paths": []}
        if not self.is_path_exists(path):
            return items
        try:
            for item in os.listdir(path):
                try:
                    # filter files, folders, and hidden files/directories.
                    if self.is_file(f"{path}/{item}") and not self.is_hidden(
                        f"{path}/{item}"
                    ):
                        items["files"].append(item)
                    elif not self.is_file(f"{path}/{item}") and not self.is_hidden(
                        f"{path}/{item}"
                    ):
                        items["folders"].append(item)
                    elif self.is_hidden(f"{path}/{item}"):
                        items["hidden"].append(item)
                    recursive_items = self.recursive_search(f"{path}/{item}")
                    items = {key: items[key] + recursive_items[key] for key in items}
                except OSError:
                    items["error_paths"].append(path)
        except (FileNotFoundError, PermissionError):
            items["error_paths"].append(path)
        return items

    def filter_by_extensions(self, items):
        """filter the files and folder to its respective extension and category."""
        extensions = {ext: [] for ext in self.args}
        extensions["others"] = []
        extensions["folders"] = items["folders"]
        extensions["error_paths"] = items["error_paths"]
        extensions["hidden"] = items["hidden"]
        files = items["files"]

        for file in files:
            ext = f".{file.split(".")[-1]}"
            if ext in extensions.keys():
                extensions[ext].append(file)
            else:
                extensions["others"].append(file)
        return extensions

    def set_path(self, path):
        """set the path to work with, if the path doesnt exist, exit the program."""
        if not self.is_path_exists(path):
            print(f"the path specified '{path}' does not exist.")
            sys.exit(1)
        return path

    def save_buffer(self, dict):
        with open("buffer.json", "w") as file:
            json.dump(dict, file)

    def load_buffer(self):
        """
        load the previous saved json file and return the files and folders.
        this would throw "no buffer found" for the first time obviously, run the program first.
        """
        try:
            with open("buffer.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(
                "buffer.json does not exist, please run the program with -r flag first."
            )
            sys.exit(1)

    def display_graph(self, extensions):
        categories = list(extensions.keys())
        values = [len(extensions[cat]) for cat in categories]
        bars = plt.bar(categories, values)

        for bar in bars:
            yval = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                yval,
                int(yval),
                ha="center",
                va="bottom",
            )

        plt.title(" ".join(sys.argv))
        plt.xlabel("Extensions")
        plt.ylabel("Length")
        plt.savefig("graph.png")
        plt.show()

    def display_number(self, extensions):
        for key, value in extensions.items():
            print(f"{key}: {len(value)}")

    def display_data(self, extensions):
        for key, value in extensions.items():
            print(f"{key}: {', '.join(value)}")

    def parse_args(self, args):
        """validate the flags in the input, then remove it to prevent it from being a file extension."""
        flags = [
            "-r",
            "--recursive",
            "-n",
            "--number",
            "-g",
            "--graph",
            "-b",
            "--buffer",
            "-h",
            "--help",
        ]
        to_remove = []

        for arg in args:
            if arg.startswith(("-", "--")) and not arg in flags:
                print(f"Invalid argument: {arg}")
                sys.exit(1)

        if "-h" in args or "--help" in args:
            self.display_help()
            sys.exit(0)

        # buffer and recursion cannot be used at the same time.
        if ("-r" in args or "--recursive" in args) and (
            "-b" in args or "--buffer" in args
        ):
            print("recursion and buffer cannot be used at the same time.")
            sys.exit(1)

        # graph and number cannot be used at the same time.
        if "-g" in args and "-n" in args:
            print("graph and number cannot be used at the same time.")
            sys.exit(1)

        # if -b is used, ignore the path, and read the buffer.
        if "-b" in args or "--buffer" in args:
            if (
                args[0] != "-b"
                and args[0] != "--buffer"
                and not args[0].startswith(("-", "--"))
            ):
                print(
                    f"path {args[0]} is ignored when using -b flag, loading the buffer.json content instead."
                )
                to_remove.append(args[0])
            self.buffer = True
            to_remove += ["-b", "--buffer"]

        if "-g" in args or "--graph" in args:
            self.graph = True
            to_remove += ["-g", "--graph"]

        if "-n" in args or "--number" in args:
            self.number = True
            to_remove += ["-n", "--number"]

        if "-r" in args or "--recursive" in args:
            print("recursion enabled.")
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
        self.args = self.parse_args(args)

        if self.buffer:
            items = self.load_buffer()
        elif self.recursive:
            items = self.recursive_search(self.path)
            self.save_buffer(items)
        else:
            items = {
                "files": [
                    f
                    for f in os.listdir(self.path)
                    if self.is_file(f) and not self.is_hidden(f)
                ],
                "folders": [
                    f
                    for f in os.listdir(self.path)
                    if not self.is_file(f) and not self.is_hidden(f)
                ],
                "hidden": [f for f in os.listdir(self.path) if self.is_hidden(f)],
                "error_paths": [],  # work on this later.
            }

        extensions = self.filter_by_extensions(items)

        if self.graph:
            self.display_graph(extensions)
        elif self.number:
            self.display_number(extensions)
        else:
            self.display_data(extensions)


if __name__ == "__main__":
    try:
        extgraph().run(sys.argv[1:])
    except IndexError:
        extgraph().run([os.getcwd()])

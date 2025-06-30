import json
import os
import sys
import argparse
from matplotlib import pyplot as plt


def is_hidden(path):
    try:
        if sys.platform.startswith("win"):
            return os.stat(path).st_file_attributes & 0x02 != 0
        else:
            return os.path.basename(path).startswith(".")
    except (FileNotFoundError, AttributeError):
        return False


def recursive_search(path):
    # https://forum.micropython.org/viewtopic.php?t=7512#p42783
    items = {"files": [], "folders": [], "hidden": [], "error_paths": []}
    if not os.path.exists(path):
        return items
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            try:
                if is_hidden(full_path):
                    items["hidden"].append(item)
                    continue

                if os.path.isfile(full_path) and not is_hidden(full_path):
                    items["files"].append(item)
                elif os.path.isdir(full_path) and not is_hidden(full_path):
                    items["folders"].append(item)

                    recursive_items = recursive_search(full_path)
                    for key in items:
                        items[key].extend(recursive_items[key])

            except OSError:
                items["error_paths"].append(path)
    except (FileNotFoundError, PermissionError):
        items["error_paths"].append(path)
    return items


def filter_by_extensions(items, args):
    extensions = {ext: [] for ext in args}
    extensions["files"] = []
    extensions["folders"] = items["folders"]
    extensions["error_paths"] = items["error_paths"]
    extensions["hidden"] = items["hidden"]
    files = items["files"]

    for file in files:
        found = False
        for ext in args:
            if file.endswith(ext):
                extensions[ext].append(file)
                found = True
                break
        if not found:
            extensions["files"].append(file)

    return extensions


def save_buffer(items, filename="buffer.json"):
    with open(filename, "w") as f:
        json.dump(items, f, indent=4)


def load_buffer(filename="buffer.json"):
    if not os.path.exists(filename):
        save_buffer(
            {"files": [], "folders": [], "hidden": [], "error_paths": []}, filename
        )
    with open(filename, "r") as f:
        return json.load(f)


def display_file_list(extensions):
    for key, files in extensions.items():
        print(f"{key}: {', '.join(files) if files else 'None'}")


def display_file_count(extensions):
    for key, files in extensions.items():
        print(f"{key}: {len(files)}")


def display_file_graph(extensions):
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


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze file extensions in directories"
    )

    # positional
    parser.add_argument(
        "pos_path",
        nargs="?",
    )

    parser.add_argument(
        "pos_extensions",
        nargs="*",
    )

    # optional
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursively traverse directories",
    )

    parser.add_argument(
        "-n",
        "--number",
        action="store_true",
        help="Display only the count of files per extension",
    )

    parser.add_argument(
        "-g", "--graph", action="store_true", help="Display results as a graph"
    )

    parser.add_argument(
        "-b",
        "--buffer",
        action="store_true",
        help="Load results from buffer.json instead of scanning",
    )

    args = parser.parse_args()
    path_arg = args.pos_path or os.getcwd()
    extension_args = args.pos_extensions
    recursive_arg = args.recursive
    num_arg = args.number
    graph_arg = args.graph
    buffer_arg = args.buffer

    if recursive_arg and buffer_arg:
        sys.exit("Cannot use both -r and -b options together.")

    if num_arg and graph_arg:
        sys.exit("Cannot use both -n and -g options together.")

    if buffer_arg and path_arg != os.getcwd():
        print(
            f"'{path_arg}' is ignored when using -b option. Values will be loaded from 'buffer.json'."
        )
    if not buffer_arg and not os.path.exists(path_arg):
        sys.exit(f"'{path_arg}' does not exist.")

    return (
        path_arg,
        extension_args,
        recursive_arg,
        num_arg,
        graph_arg,
        buffer_arg,
    )

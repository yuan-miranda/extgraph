import os
import sys
import json
import argparse
import matplotlib.pyplot as plt


def is_hidden(path):
    try:
        return os.stat(path).st_file_attributes & 0x02 != 0
    except FileNotFoundError:
        return False


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


def recursive_search(path):
    """recursively traverse the directory. Based on Roberthh's implementation: https://forum.micropython.org/viewtopic.php?t=7512#p42783."""
    items = {"files": [], "folders": [], "hidden": [], "error_paths": []}
    if not is_path_exists(path):
        return items
    try:
        for item in os.listdir(path):
            try:
                # filter files, folders, and hidden files/directories.
                if is_file(f"{path}/{item}") and not is_hidden(f"{path}/{item}"):
                    items["files"].append(item)
                elif not is_file(f"{path}/{item}") and not is_hidden(f"{path}/{item}"):
                    items["folders"].append(item)
                elif is_hidden(f"{path}/{item}"):
                    items["hidden"].append(item)
                recursive_items = recursive_search(f"{path}/{item}")
                items = {key: items[key] + recursive_items[key] for key in items}
            except OSError:
                items["error_paths"].append(path)
    except (FileNotFoundError, PermissionError):
        items["error_paths"].append(path)
    return items


def filter_by_extensions(items, args):
    """filter the files and folder to its respective extension and category."""
    extensions = {ext: [] for ext in args}
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


def save_buffer(dict):
    with open("buffer.json", "w") as file:
        json.dump(dict, file)


def load_buffer():
    """
    load the previous saved json file and return the files and folders.
    this would throw "no buffer found" for the first time obviously, run the program first.
    """
    try:
        with open("buffer.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("buffer.json does not exist, please run the program with -r flag first.")
        sys.exit(1)


def display_graph(extensions):
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


def display_number(extensions):
    for key, value in extensions.items():
        print(f"{key}: {len(value)}")


def display_data(extensions):
    for key, value in extensions.items():
        print(f"{key}: {', '.join(value)}")


def create_parser():
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Analyze file extensions in directories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  extgraph.py /path/to/directory -r -g .py .js
  extgraph.py -b -n .txt .md
  extgraph.py . --recursive --number
        """,
    )

    # Positional argument for path
    parser.add_argument(
        "pos_path",
        nargs="?",
        default=os.getcwd(),
        help="Directory path to analyze (default: current directory)",
    )

    # Positional arguments for extensions
    parser.add_argument(
        "pos_extensions",
        nargs="*",
        help="File extensions to filter (e.g., .py .js .txt)",
    )

    # Optional flags
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

    return parser


def validate_args(args):
    """Validate argument combinations and handle conflicts."""
    # Buffer and recursive cannot be used together
    if args.recursive and args.buffer:
        print("Error: recursion and buffer cannot be used at the same time.")
        sys.exit(1)

    # Graph and number cannot be used together
    if args.graph and args.number:
        print("Error: graph and number cannot be used at the same time.")
        sys.exit(1)

    # If buffer is used, ignore the path
    if args.buffer and args.pos_path != os.getcwd():
        print(
            f"Warning: path '{args.pos_path}' is ignored when using -b flag, loading buffer.json content instead."
        )

    # Validate path exists (unless using buffer)
    if not args.buffer:
        if not is_path_exists(args.pos_path):
            print(f"Error: the path specified '{args.pos_path}' does not exist.")
            sys.exit(1)

    if args.recursive:
        print("recursion enabled.")


def parse_args(args_list):
    """Parse command line arguments using argparse."""
    parser = create_parser()
    args = parser.parse_args(args_list)
    validate_args(args)

    return (
        args.pos_extensions,
        args.graph,
        args.number,
        args.recursive,
        args.buffer,
        args.pos_path,
    )


def main(args_list):
    extension_args, graph, number, recursive, buffer, path = parse_args(args_list)

    if buffer:
        items = load_buffer()
    elif recursive:
        items = recursive_search(path)
        save_buffer(items)
    else:
        items = {
            "files": [
                f
                for f in os.listdir(path)
                if is_file(os.path.join(path, f))
                and not is_hidden(os.path.join(path, f))
            ],
            "folders": [
                f
                for f in os.listdir(path)
                if not is_file(os.path.join(path, f))
                and not is_hidden(os.path.join(path, f))
            ],
            "hidden": [f for f in os.listdir(path) if is_hidden(os.path.join(path, f))],
            "error_paths": [],  # work on this later.
        }

    extensions = filter_by_extensions(items, extension_args)

    if graph:
        display_graph(extensions)
    elif number:
        display_number(extensions)
    else:
        display_data(extensions)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except IndexError:
        main([os.getcwd()])

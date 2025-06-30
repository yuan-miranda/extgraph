import os
import matplotlib.pyplot as plt
from main import (
    is_hidden,
    parse_args,
    recursive_search,
    load_buffer,
    save_buffer,
    filter_by_extensions,
    display_file_graph,
    display_file_count,
    display_file_list,
)


def main():
    path_arg, extension_args, recursive_arg, num_arg, graph_arg, buffer_arg = (
        parse_args()
    )

    if buffer_arg:
        items = load_buffer()
    elif recursive_arg:
        items = recursive_search(path_arg)
        save_buffer(items)
    else:
        items = {
            "files": [
                f
                for f in os.listdir(path_arg)
                if os.path.isfile(os.path.join(path_arg, f))
                and not is_hidden(os.path.join(path_arg, f))
            ],
            "folders": [
                f
                for f in os.listdir(path_arg)
                if os.path.isdir(os.path.join(path_arg, f))
                and not is_hidden(os.path.join(path_arg, f))
            ],
            "hidden": [
                f for f in os.listdir(path_arg) if is_hidden(os.path.join(path_arg, f))
            ],
            "error_paths": [],
        }

    extensions = filter_by_extensions(items, extension_args)

    if graph_arg:
        display_file_graph(extensions)
    elif num_arg:
        display_file_count(extensions)
    else:
        display_file_list(extensions)


if __name__ == "__main__":
    main()

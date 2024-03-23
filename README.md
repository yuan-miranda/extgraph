## Extension Graph (extgraph)
A python script that can list, filter files based on its extension.

> [extgraph.py](https://github.com/yuan-miranda/extgraph/blob/main/extgraph.py) source code for the script.

## Usage
Recursively access every content of the directory, and/or list in number quantity instead of each file, filter it by extension name i.e. `.txt`.
```
py extgraph.py <path> [-r] [-n] [extension1 .extension2 ...]
```
Read the buffer (last script execution content), and/or list in number quantity instead of each file, filter it by extension name i.e. `.txt`.
```
py extgraph.py [-b] [-n] [extension1 .extension2 ...]
```
Show usage guide or version.
```
py extgraph.py [-h] [-v]
```
By default this will list the current directory content.
```
py extgraph.py
```

## Example Commands

| Command                     | Operation                                                                 |
|-----------------------------|---------------------------------------------------------------------------|
| `py extgraph.py`            | List the current directory content                                        |
| `py extgraph.py ..`         | List the parent directory content                                         |
| `py extgraph.py .. -n`      | List the parent directory in number quantity instead of each file         |
| `py extgraph.py -r`         | List all the content of current directory recursively                     |
| `py extgraph.py -b`         | List the content of the buffer                                            |
| `py extgraph.py .. -b`      | (Invalid) .. is ignored, and will only read the content of the buffer     |
| `py extgraph.py -v`         | Display the current version of the script                                 |

No need to setup things, you can even copy paste the source code alone and this will run (unless you dont have the packages used in this script which is wierd because its pre-intalled by dafault).

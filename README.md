## Extension Graph (extgraph)
A python script that can list, filter files based on its extension.
> [extgraph.py](https://github.com/yuan-miranda/extgraph/blob/main/extgraph.py) source code for the script.

## Usage
Recursively accesses the contents of a directory, listing them in the terminal or generating a GUI graph. You can filter the files by extension name (e.g., .txt).
```
py extgraph.py <path> [-r] [-n | -g] [extension1 .extension2 ...]
```
Read the buffer (content from the last script execution) and/or list files in the terminal or generate a GUI graph, filtered by extension name.
```
py extgraph.py [-b] [-n | -g] [extension1 .extension2 ...]
```
To display the usage guide or version information.
```
py extgraph.py [-h] [-v]
```
By default, the script lists the contents of the current directory.
```
py extgraph.py
```

## Example Commands
| Command                   | Operation                                                                 |
|---------------------------|---------------------------------------------------------------------------|
| py extgraph.py            | Lists the content of the current directory                                |
| py extgraph.py ..         | Lists the content of the parent directory                                 |
| py extgraph.py .. -n      | Lists the content of the parent directory, displaying the number of files |
| py extgraph.py -r         | Lists all the contents of the current directory recursively               |
| py extgraph.py -b         | Lists the content of the buffer                                           |
| py extgraph.py .. -b      | (Invalid) ".." is ignored, and only the content of the buffer is read     |
| py extgraph.py -v         | Displays the current version of the script                                |
| py extgraph.py -g         | Generate and display a graphical graph of the data                        |

## Installation:
**Note: You must have `Git` and `Python 3` or above installed prior to this setup.**
1. Clone the repository on your machine:
> Note: No need to clone the repository, you can even just download or copy the contents of [extgraph.py](https://github.com/yuan-miranda/extgraph/blob/main/extgraph.py) and it will still work fine.<br>
```
git clone https://github.com/yuan-miranda/extgraph.git
```
2. Download the following modules:
```
pip install os sys json matplotlib
```
3. Run the script by executing the command below:
```
python microfilesys.py
```

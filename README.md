# Extension Graph (extgraph)

A python script that can list, filter, visualize files and directiories based on its extension.

## Install

Clone the repository and install the dependencies

```
https://github.com/yuan-miranda/extgraph.git
```

```
cd extgraph
```

```
pip install -r requirements.txt
```

## Usage

### For a generic help page

```
python .\extgraph.py --help
```

List the files in the current directory

```
py .\extgraph.py
```

List the files recursively in the current directory (all files)

```
py .\extgraph.py --recursive
```

List in file count (i.e., folder: 10)

```
py .\extgraph.py --number
```

List the file in a bar graph using matplotlib

```
py .\extgraph.py --graph
```

Load the value from the buffer.json

```
py .\extgraph.py --buffer
```

## Contributing

PRs accepted.

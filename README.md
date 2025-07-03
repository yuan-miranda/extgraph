# Extension Graph (extgraph)

A python script that can list, filter, visualize files and directiories based on its extension.
![image](https://github.com/user-attachments/assets/da0e5e8d-8c7a-4555-a076-45e63ed294f2)

## Install

Clone the repository and install the dependencies

```
git clone https://github.com/yuan-miranda/extgraph.git
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
python .\extgraph.py
```

List the files recursively in the current directory (all files)

```
python .\extgraph.py --recursive
```

List in file count (i.e., folder: 10)

```
python .\extgraph.py --number
```

List the file in a bar graph using matplotlib

```
python .\extgraph.py --graph
```

Load the value from the buffer.json

```
python .\extgraph.py --buffer
```

Separate the specified extensions

```
python .\extgraph.py . .py
```

## Contributing

PRs accepted.

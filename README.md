
# Red-Black Tree Implementation

This Python project implements a space-saving red-black tree for managing key-value pairs. 
The red-black tree is a self-balancing binary search tree with constraints that maintain 
tree balance and optimize search, insertion, and deletion operations.

## Features

- **Node Representation:** Each node in the tree has the following attributes:
  - `key`: The unique identifier for the node.
  - `value`: The data associated with the node.
  - `colour`: Specifies if the node is `Red` or `Black`.
  - `left` and `right`: Pointers to the child nodes.

- **Tree Operations:**
  - Search for a key in the tree.
  - Add new key-value pairs while maintaining red-black tree properties.
  - Update or replace child nodes dynamically.

- **Constants and Utility Functions:**
  - Defines `Red` and `Black` to represent node colors.
  - Utility functions for child node management, branch labels, and tree traversal.

## Getting Started

### Prerequisites

- Python 3.6 or higher.

### Usage

1. Clone this repository or download the `red_black.py` file.
2. Import the `Node` class into your Python project to start using red-black trees:

```python
from red_black import Node

# Example: Creating a new node
node = Node(key=1, value='example')
print(node)
```

3. Use the provided methods to build, search, and manipulate the tree.

### Example Usage

Below is a basic example of using the red-black tree:

```python
# Create a new root node
root = Node(key=10, value="Root")

# Add child nodes
left_child = Node(key=5, value="Left Child")
right_child = Node(key=15, value="Right Child")

root.setChild(0, left_child)  # Set left child
root.setChild(1, right_child)  # Set right child

# Search for a key
result = root.search(15)
print("Search Result:", result)
```

## Code Structure

- **Node class:** Implements the fundamental structure and methods for tree nodes.
- **Utility functions:** Helper functions for managing tree branches and colors.

## Author

- **John Longley** - October 2022

This file was originally developed for the Inf2-IADS course (2022-23) as part of Coursework 1, Part B.

## License

This project does not include a license. Contact the author for permission to reuse the code.

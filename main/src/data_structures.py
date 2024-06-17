import heapq
from collections import deque

class MinHeap:
    """Simple min-heap implementation using Python's heapq module."""
    def __init__(self):
        """Initialize a new empty min-heap."""
        self.heap = []  # List to store the heap elements

    def insert(self, item):
        """Insert an item into the heap."""
        heapq.heappush(self.heap, item)

    def remove_min(self):
        """Remove and return the smallest item from the heap. Returns None if the heap is empty."""
        if not self.heap:
            return None
        return heapq.heappop(self.heap)

    def get_min(self):
        """Return the smallest item from the heap without removing it. Returns None if the heap is empty."""
        if not self.heap:
            return None
        return self.heap[0]

    def is_empty(self):
        """Check if the heap is empty. Returns True if empty, False otherwise."""
        return len(self.heap) == 0

class Stack:
    """Simple stack implementation with basic LIFO (Last In, First Out) operations."""
    def __init__(self):
        """Initialize a new empty stack."""
        self.items = []  # List to store stack items

    def push(self, item):
        """Push an item onto the stack."""
        self.items.append(item)

    def pop(self):
        """Remove and return the top item of the stack. Returns None if the stack is empty."""
        return self.items.pop() if self.items else None

    def peek(self):
        """Return the top item of the stack without removing it. Returns None if the stack is empty."""
        return self.items[-1] if self.items else None

    def is_empty(self):
        """Check if the stack is empty. Returns True if empty, False otherwise."""
        return len(self.items) == 0
    
class Node:
    """Node class for LinkedList elements."""
    def __init__(self, value):
        self.value = value  # The value stored in the node
        self.next = None    # Pointer to the next node in the list

class LinkedList:
    """Enhanced linked list with additional complex operations."""
    def __init__(self):
        self.head = None  # Start with an empty list

    def append(self, value):
        """Append a new node with the specified value to the end of the list."""
        if not self.head:
            self.head = Node(value)  # If the list is empty, set the new node as the head
        else:
            current = self.head
            while current.next:  # Traverse to the end of the list
                current = current.next
            current.next = Node(value)  # Create a new node at the end of the list

    def remove(self, value):
        """Remove the first occurrence of the specified value from the list."""
        current = self.head
        previous = None
        while current and current.value != value:
            previous = current  # Keep track of the previous node
            current = current.next
        if current is None:  # If the value was not found
            return False
        if previous is None:  # If the node to be removed is the head
            self.head = self.head.next
        else:
            previous.next = current.next  # Bypass the current node
        return True
    
    def reverse(self):
        """Reverse the linked list in place."""
        prev = None
        current = self.head
        while current:
            next_node = current.next  # store reference to the next node
            current.next = prev  # reverse the current node's pointer
            prev = current  # move prev and current one step forward
            current = next_node
        self.head = prev

    def find_middle(self):
        """Find and return the middle node of the linked list using the fast and slow pointer technique."""
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def sort(self):
        """Sort the linked list using merge sort algorithm."""
        def merge(left, right):
            if not left:
                return right
            if not right:
                return left

            if left.data < right.data:
                left.next = merge(left.next, right)
                return left
            else:
                right.next = merge(left, right.next)
                return right

        def merge_sort(node):
            if not node or not node.next:
                return node

            middle = self.find_middle()
            next_to_middle = middle.next
            middle.next = None

            left = merge_sort(node)
            right = merge_sort(next_to_middle)

            sorted_list = merge(left, right)
            return sorted_list

        self.head = merge_sort(self.head)

    def display(self):
        """Display all values in the list."""
        current = self.head
        values = []
        while current:
            values.append(current.value)
            current = current.next
        return values
    
class Vector:
    """A dynamic array-like data structure that mimics vector behavior."""
    def __init__(self):
        self.items = []
        self.capacity = 10
        self.size = 0

    def push_back(self, item):
        """Add an item to the end of the vector, resizing if necessary."""
        if self.size >= self.capacity:
            self._resize()
        self.items.append(item)
        self.size += 1

    def pop_back(self):
        """Remove the last item of the vector and return it."""
        if self.size == 0:
            raise IndexError("pop_back from empty vector")
        self.size -= 1
        return self.items.pop()

    def _resize(self):
        """Resize the internal storage of the vector."""
        self.capacity *= 2
        new_items = [None] * self.capacity
        for i in range(self.size):
            new_items[i] = self.items[i]
        self.items = new_items

    def __str__(self):
        """Return a string representation of the vector."""
        return str(self.items[:self.size])

class Array:
    """A fixed-size array structure, mimicking static array behavior from languages like C."""
    
    def __init__(self, size, initial_value=None):
        """Initialize the array with a given size and an initial value for each element."""
        self.size = size
        self.items = [initial_value] * size

    def set_item(self, index, value):
        """Set the value at the specified index, throwing an error if the index is out of bounds."""
        if index >= self.size or index < 0:
            raise IndexError("Array index out of bounds")
        self.items[index] = value

    def get_item(self, index):
        """Retrieve an item from an array with error handling for index out of bounds."""
        try:
            return self.items[index]
        except IndexError:
            raise IndexError("Attempted to access index out of the defined range.")


class Queue:
    """Simple FIFO (First In, First Out) queue implementation."""
    def __init__(self):
        """Initialize a new empty queue."""
        self.items = []  # List to store queue items

    def enqueue(self, item):
        """Add an item to the end of the queue."""
        self.items.append(item)

    def dequeue(self):
        """Remove and return the front item of the queue. Returns None if the queue is empty."""
        if not self.items:
            return None
        return self.items.pop(0)

    def is_empty(self):
        """Check if the queue is empty. Returns True if empty, False otherwise."""
        return len(self.items) == 0

    def peek(self):
        """Return the front item of the queue without removing it. Returns None if the queue is empty."""
        if not self.items:
            return None
        return self.items[0]

class PriorityQueue:
    """A simple priority queue implementation using a heap."""
    def __init__(self):
        """Initialize a new empty priority queue."""
        self.heap = []  # List to store the heap items

    def enqueue(self, item, priority):
        """Add an item with a given priority to the queue."""
        # The heapq module uses min-heap by default, so we use negative priority to simulate a max-heap
        heapq.heappush(self.heap, (-priority, item))

    def dequeue(self):
        """Remove and return the item with the highest priority. Returns None if the queue is empty."""
        if not self.heap:
            return None
        return heapq.heappop(self.heap)[1]

    def peek(self):
        """Return the item with the highest priority without removing it. Returns None if the queue is empty."""
        if not self.heap:
            return None
        return self.heap[0][1]

    def is_empty(self):
        """Check if the priority queue is empty. Returns True if empty, False otherwise."""
        return len(self.heap) == 0

class HashTable:
    """Simple hash table implementation using Python's built-in dictionary."""
    def __init__(self):
        """Initialize a new empty hash table."""
        self.table = {}  # Dictionary to store key-value pairs

    def set_item(self, key, value):
        """Add a key-value pair to the hash table, or update the value if the key already exists."""
        self.table[key] = value

    def get_item(self, key):
        """Retrieve the value associated with a key. Returns None if the key does not exist."""
        return self.table.get(key, None)

    def remove_item(self, key):
        """Remove a key-value pair from the hash table. Returns the value if the key existed, None otherwise."""
        return self.table.pop(key, None)

    def contains_key(self, key):
        """Check if a key exists in the hash table. Returns True if the key exists, False otherwise."""
        return key in self.table

    def is_empty(self):
        """Check if the hash table is empty. Returns True if empty, False otherwise."""
        return not bool(self.table)

class TreeNode:
    """Node of a binary tree containing some data, and left and right children."""
    def __init__(self, data):
        """Initialize a tree node with data, and no children."""
        self.data = data
        self.left = None
        self.right = None

class BinaryTree:
    """Simple binary tree implementation."""
    def __init__(self):
        """Initialize an empty binary tree."""
        self.root = None

    def insert(self, data):
        """Insert data into the binary tree."""
        if self.root is None:
            self.root = TreeNode(data)
        else:
            self._insert(self.root, data)

    def _insert(self, node, data):
        """Helper method to insert data recursively."""
        if data < node.data:  # Data goes to the left subtree
            if node.left is None:
                node.left = TreeNode(data)
            else:
                self._insert(node.left, data)
        else:  # Data goes to the right subtree
            if node.right is None:
                node.right = TreeNode(data)
            else:
                self._insert(node.right, data)

    def inorder_traversal(self, node=None):
        """Perform in-order traversal of the tree and return the elements in a list."""
        if node is None:
            node = self.root
        elements = []
        if node:
            elements += self.inorder_traversal(node.left)
            elements.append(node.data)
            elements += self.inorder_traversal(node.right)
        return elements

class BinarySearchTree:
    """Binary search tree implementation."""
    def __init__(self):
        """Initialize an empty BST."""
        self.root = None

    def insert(self, data):
        """Insert data into the BST, maintaining BST properties."""
        self.root = self._insert(self.root, data)

    def _insert(self, node, data):
        """Recursive helper method to insert data into the BST."""
        if node is None:
            return TreeNode(data)
        elif data < node.data:
            node.left = self._insert(node.left, data)
        else:
            node.right = self._insert(node.right, data)
        return node

    def search(self, data):
        """Search for data in the BST. Return True if the data is found, otherwise False."""
        return self._search(self.root, data)

    def _search(self, node, data):
        """Recursive helper method to search for data in the BST."""
        if node is None:
            return False
        elif data == node.data:
            return True
        elif data < node.data:
            return self._search(node.left, data)
        else:
            return self._search(node.right, data)

    def inorder_traversal(self, node=None):
        """In-order traversal of the BST that returns sorted order of elements."""
        if node is None:
            node = self.root
        elements = []
        if node:
            elements += self.inorder_traversal(node.left)
            elements.append(node.data)
            elements += self.inorder_traversal(node.right)
        return elements

class Graph:
    """Extended graph class with additional algorithms."""
    def __init__(self):
        """Initialize an empty graph."""
        self.adj_list = {}  # Dictionary to store the adjacency list of each vertex

    def add_vertex(self, vertex):
        """Add a vertex to the graph."""
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, vertex1, vertex2, bidirectional=True):
        """Add an edge between two vertices. If bidirectional is True, add an undirected edge."""
        if vertex1 not in self.adj_list:
            self.add_vertex(vertex1)
        if vertex2 not in self.adj_list:
            self.add_vertex(vertex2)
        self.adj_list[vertex1].append(vertex2)
        if bidirectional:
            self.adj_list[vertex2].append(vertex1)

    def get_neighbors(self, vertex):
        """Return the list of all neighbors of a given vertex."""
        return self.adj_list.get(vertex, [])

    def display(self):
        """Display the graph as adjacency list."""
        for vertex, neighbors in self.adj_list.items():
            print(f"{vertex}: {neighbors}")

    def dfs(self, start_vertex, visited=None):
        """Depth-first search (DFS) algorithm to visit all vertices reachable from start_vertex."""
        if visited is None:
            visited = set()
        visited.add(start_vertex)
        print(start_vertex, end=' ')
        for neighbor in self.get_neighbors(start_vertex):
            if neighbor not in visited:
                self.dfs(neighbor, visited)

    def bfs(self, start_vertex):
        """Breadth-first search (BFS) algorithm to visit all vertices level by level from start_vertex."""
        visited = set()
        queue = deque([start_vertex])
        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                print(vertex, end=' ')
                visited.add(vertex)
                for neighbor in self.get_neighbors(vertex):
                    if neighbor not in visited:
                        queue.append(neighbor)
    
    def dijkstra(self, start_vertex):
        """Find the shortest path from start_vertex to all other vertices using Dijkstra's algorithm."""
        distances = {vertex: float('infinity') for vertex in self.adj_list}
        distances[start_vertex] = 0
        priority_queue = [(0, start_vertex)]
        
        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            # Nodes can only be added once to the priority queue
            if current_distance > distances[current_vertex]:
                continue

            for neighbor in self.adj_list[current_vertex]:
                distance = current_distance + 1  # assuming all edges have weight 1
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
                    
        return distances

    def has_cycle(self):
        """Check if the graph contains a cycle."""
        def visit(vertex, visited, rec_stack):
            visited.add(vertex)
            rec_stack.add(vertex)

            for neighbor in self.adj_list[vertex]:
                if neighbor not in visited:
                    if visit(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(vertex)
            return False

        visited, rec_stack = set(), set()
        for v in self.adj_list:
            if v not in visited:
                if visit(v, visited, rec_stack):
                    return True
        return False

class AVLNode(TreeNode):
    """Node for an AVL tree, which extends TreeNode with a height attribute for balancing."""
    def __init__(self, data):
        super().__init__(data)
        self.height = 1  # height of node in the tree

class AVLTree(BinarySearchTree):
    """Self-balancing binary search tree using AVL rotations."""
    def _update_height(self, node):
        """Update the height of a node based on heights of its children."""
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    def _get_height(self, node):
        """Get the height of a node, return 0 if the node is None."""
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        """Get the balance factor of a node, the difference between the heights of the left and right subtrees."""
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_left(self, z):
        """Perform a left rotation around the given node z."""
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        self._update_height(z)
        self._update_height(y)
        return y  # new root

    def _rotate_right(self, z):
        """Perform a right rotation around the given node z."""
        y = z.left
        T2 = y.right
        y.right = z
        z.left = T2
        self._update_height(z)
        self._update_height(y)
        return y  # new root

    def _insert(self, node, data):
        """Insert a node and perform AVL rebalancing."""
        if not node:
            return AVLNode(data)
        elif data < node.data:
            node.left = self._insert(node.left, data)
        else:
            node.right = self._insert(node.right, data)
        
        self._update_height(node)
        balance = self._get_balance(node)

        # Left Left Case
        if balance > 1 and data < node.left.data:
            return self._rotate_right(node)
        # Right Right Case
        if balance < -1 and data > node.right.data:
            return self._rotate_left(node)
        # Left Right Case
        if balance > 1 and data > node.left.data:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        # Right Left Case
        if balance < -1 and data < node.right.data:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

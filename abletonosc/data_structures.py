import os
import sys
import pickle
import json

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

class TreeNode:
    def __init__(self, name, node_type, children=None):
        self.name = name
        self.node_type = node_type
        self.children = children if children is not None else []

    def is_leaf(self):
        return len(self.children) == 0

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"TreeNode(name={self.name}, node_type={self.node_type}, children={self.children})"

class LiveDeviceTree:
    def __init__(self, root=None):
        self.root = root
        if root is not None:
            self.tree = self.build_tree(self.root)
        else:
            self.tree = None

    def build_tree(self, root):
        def traverse(node):
            try:
                name = node.name
            except AttributeError:
                return None
            name = node.name
            node_type = 'instrument'  # Customize this if there are other types
            tree_node = TreeNode(name, node_type)
            
            for child in node.children:
                child_tree_node = traverse(child)
                if child_tree_node is not None:
                    tree_node.add_child(child_tree_node)
            
            return tree_node

        return traverse(root)

    def merge_tree(self, other_tree):
        if self.tree is None:
            self.tree = other_tree.tree
        else:
            self._merge_nodes(self.tree, other_tree.tree)

    def _merge_nodes(self, node1, node2):
        if node1 is None:
            return node2
        if node2 is None:
            return node1
        for child in node2.children:
            existing_child = next((n for n in node1.children if n.name == child.name), None)
            if existing_child:
                self._merge_nodes(existing_child, child)
            else:
                node1.add_child(child)

    def get_leaf_nodes(self):
        leaves = []

        def traverse(node):
            if node.is_leaf():
                leaves.append(node)
            else:
                for child in node.children:
                    traverse(child)

        traverse(self.tree)
        return leaves
    
    def get_nodes_by_name(self, name):
        nodes = []

        def traverse(node):
            if node.name == name:
                nodes.append(node)
            for child in node.children:
                traverse(child)

        traverse(self.tree)
        return nodes

    def get_nodes_by_type(self, node_type):
        nodes = []

        def traverse(node):
            if node.node_type == node_type:
                nodes.append(node)
            for child in node.children:
                traverse(child)

        traverse(self.tree)
        return nodes
    
    def get_nodes_by_parent(self, parent_names, leaf_only=True):
        nodes = []
        def traverse(node, parent_chain=None):
            if parent_chain and set(parent_names).issubset(set(parent.name for parent in parent_chain)):
                if leaf_only and not node.is_leaf():
                    return
                nodes.append(node)
            parent_chain = parent_chain + [node] if parent_chain else [node]
            for child in node.children:
                traverse(child, parent_chain=parent_chain)
        traverse(self.tree)
        return nodes

    def save_tree(self, filename=None):
        if filename:
            with open(filename, 'wb') as f:
                pickle.dump(self.tree, f)
        else:
            return pickle.dumps(self.tree)

    def load_tree_from_file(self, filename):
        with open(filename, 'rb') as f:
            self.tree = pickle.load(f)

    def load_tree_from_bytes(self, data):
        self.tree = pickle.loads(data)

    def find_corresponding_node(self, other_tree, node_name):
        def traverse(other_node):
            if node_name == other_node.name and len(other_node.children) == 0:
                return other_node
            for other_child in other_node.children:
                result = traverse(other_child)
                if result:
                    return result
            return None
        
        if self.tree and other_tree:
            return traverse(other_tree)
        else:
            return None
        
    def to_json(self):
        def traverse(node):
            if node.is_leaf():
                return {
                    'name': node.name,
                    'type': node.node_type,
                    'children': []
                }
            else:
                return {
                    'name': node.name,
                    'type': node.node_type,
                    'children': [traverse(child) for child in node.children]
                }
        
        return traverse(self.tree)

    def __repr__(self):
        def traverse(node, indent=""):
            result = ""
            if node.is_leaf():
                result += f"{indent}└── {node.name}\n"
            else:
                result += f"{indent}├── {node.name}\n"
                for i, child in enumerate(node.children):
                    if i == len(node.children) - 1:
                        result += traverse(child, indent + "    ")
                    else:
                        result += traverse(child, indent + "│   ")
            return result
        
        return traverse(self.tree)
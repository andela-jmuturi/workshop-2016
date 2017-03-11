class BinaryTree:
    """Represent a binary tree using nodes and references.

    Each binary tree has a root node that stores a value labelled as its key,
    a left child and a right child that are either empty or contain another
    binary tree each.
    """
    def __init__(self, root_value):
        self.key = root_value
        self.right_child = None
        self.left_child = None

    def __repr__(self):
        return f'<BinaryTree: "{self.key}">'

    def insert_right(self, new_node):
        new_subtree = BinaryTree(new_node)
        if self.right_child is None:
            self.right_child = new_subtree
        else:
            new_subtree.right_child = self.right_child
            self.right_child = new_subtree

    def insert_left(self, new_node):
        new_subtree = BinaryTree(new_node)
        if self.left_child is None:
            self.left_child = new_subtree
        else:
            new_subtree.left_child = self.left_child
            self.left_child = new_subtree

    def set_root_value(self, value):
        self.key = value

    def get_root_value(self):
        return self.key

    def get_left_child(self):
        return self.left_child

    def get_right_child(self):
        return self.right_child


def build_tree():
    b = BinaryTree('a')
    b.insert_left('b')
    b.get_left_child().insert_right('d')
    b.insert_right('c')
    b.get_right_child().insert_left('e')
    b.get_right_child().insert_right('f')
    return b


def test_equal(actual, expected):
    if actual == expected:
        print('Pass')
    else:
        print(f'Fail: Expected "{actual}" to equal "{expected}"')

if __name__ == '__main__':
    ttree = build_tree()
    test_equal(ttree.get_right_child().get_root_value(), 'c')
    test_equal(ttree.get_left_child().get_right_child().get_root_value(), 'd')
    test_equal(ttree.get_right_child().get_left_child().get_root_value(), 'e')

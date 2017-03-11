def BinaryTree(r):
    """Represent a binary tree using a list of lists.

    The first item in the list is the root node. The second item
    is its left leaf node. The third is the right leaf node.
    """
    return [r, [], []]


def insert_left(root, new_branch):
    """
    Given a root node and a new branch, insert the new branch as the left
    leaf of the root node.
    """
    subtree = root.pop(1)
    if subtree:
        # If the old left child had something in it, make it the left node of
        # the new left node.
        root.insert(1, [new_branch, subtree, []])
    else:
        root.insert(1, [new_branch, [], []])
    return root


def insert_right(root, new_branch):
    """
    Given a root node and a new branch, insert the new branch as the right
    leaf of the root node.
    """
    subtree = root.pop(2)
    if subtree:
        # If the old right node has sth, make it the right node of the new leaf.
        root.insert(2, [new_branch, [], subtree])
    else:
        root.insert(2, [new_branch, [], []])
    return root


def get_root_value(root):
    """Return the value of the root node"""
    return root[0]


def set_root_value(root, value):
    """Set a value to the root node."""
    root[0] = value
    return root


def get_left_child(root):
    """Given a root node, return it's left child"""
    return root[1]


def get_right_child(root):
    """Given a root node, return it's right child"""
    return root[2]

def main():
    r = BinaryTree(3)
    insert_left(r, 4)
    insert_left(r, 5)
    insert_right(r, 6)
    insert_right(r, 7)
    left = get_left_child(r)
    print(f'left: {left}')

    set_root_value(left, 9)
    print(f'root: {r}')

    insert_left(left, 11)
    print(f'root: {r}')

    print(f'get_right_child(get_right_child(root)): {get_right_child(get_right_child(r))}')

if __name__ == '__main__':
    main()

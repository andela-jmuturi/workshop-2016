import operator as op

from trees.binary_tree_nodes_refs import BinaryTree
from .parse_tree import build_parse_tree


def preorder(tree: BinaryTree):
    """Preorder tree traversal implemented as an external function"""
    if tree:
        print(tree.get_root_value())
        preorder(tree.get_left_child())
        preorder(tree.get_right_child())


def postorder(tree: BinaryTree):
    """Postorder tree traversal"""
    if tree is not None:
        postorder(tree.get_left_child())
        postorder(tree.get_right_child())
        print(tree.get_root_value())


def postordereval(tree: BinaryTree):
    """BinaryTree evaluation using postorder traversal."""
    ops = {
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.truediv
    }
    left_result = right_result = None
    if tree:
        left_result = postordereval(tree.get_left_child())
        right_result = postordereval(tree.get_right_child())
        root_value = tree.get_root_value()
        if left_result and right_result:
            return ops[root_value](left_result, right_result)
        return root_value


def inorder(tree: BinaryTree):
    """Inorder tree traversal"""
    if tree is not None:
        inorder(tree.get_left_child())
        print(tree.get_root_value())
        inorder(tree.get_right_child())


def construct_expression(tree: BinaryTree):
    """
    Use inorder tree traversal to reconstruct a fully parenthesized
    expression from a binary tree.
    """
    expr = []
    previous = None
    def get_parenthesis(node, parenthesis):
        nonlocal previous
        previous = parenthesis

        has_parens = False
        if node:
            value = node.get_root_value()
            has_parens = previous or not isinstance(value, int)
        return parenthesis if has_parens else ''

    if tree:
        left_result = tree.get_left_child()
        right_result = tree.get_right_child()

        expr = [
            get_parenthesis(left_result, '('),
            construct_expression(left_result),
            str(tree.get_root_value()),
            construct_expression(right_result),
            get_parenthesis(right_result, ')')
        ]
    return ''.join(expr)


def main():
    t = build_parse_tree('( ( 10 + 5 ) * ( 3 / 10 ) )')
    print(f'postordereval: {postordereval(t)}')
    print(f'expression: {construct_expression(t)}')


if __name__ == '__main__':
    main()

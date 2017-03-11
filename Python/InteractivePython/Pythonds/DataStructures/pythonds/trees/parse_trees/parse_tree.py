import operator

from basics.stack import Stack
from trees.binary_tree_nodes_refs import BinaryTree


def build_parse_tree(fpexp: str):
    """Build a parse tree from a fully-parenthesized expression."""
    fplist = fpexp.split()
    p_stack = Stack()
    e_tree = BinaryTree('')
    p_stack.push(e_tree)
    current_tree = e_tree

    for i in fplist:
        if i == '(':
            current_tree.insert_left('')
            p_stack.push(current_tree)
            current_tree = current_tree.get_left_child()
        elif i not in ['+', '-', '*', '/', ')']:
            current_tree.set_root_value(int(i))
            parent = p_stack.pop()
            current_tree = parent
        elif i in ['+', '-', '*', '/']:
            current_tree.set_root_value(i)
            current_tree.insert_right('')
            p_stack.push(current_tree)
            current_tree = current_tree.get_right_child()
        elif i == ')':
            current_tree = p_stack.pop()
        else:
            raise ValueError(f'Invalid token: {i}')
    return e_tree


def evaluate(parse_tree: BinaryTree):
    """Evaluate a parse tree and return it's arithmetic value"""
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    left_child = parse_tree.get_left_child()
    right_child = parse_tree.get_right_child()

    if left_child and right_child:
        fn = operators[parse_tree.get_root_value()]
        return fn(evaluate(left_child), evaluate(right_child))
    return parse_tree.get_root_value()


def main():
    pt = build_parse_tree('( ( 10 + 5 ) * 3 )')
    print(f'pt: {pt}')
    value = evaluate(pt)
    print(f'value: {value}')


if __name__ == '__main__':
    main()

"""
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file. If not, see <http://www.gnu.org/licenses/>.
"""
from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree

def build_tree(formula):
    if len(formula) is 1 and formula in "abcdefghijklmnopqrstuvwxyz":
        node = Leaf(formula)

    else:
        if len(formula) > 1 and formula[0] == "(" and formula[-1] == ")":
            formula = formula[1:-1]
            connective_found = False
            counter = 0
            found_L_brac = False
            while not connective_found:

                if counter >= len(formula):
                    node = None
                    connective_found = True

                elif found_L_brac and formula[counter] is ")":
                    found_L_brac = False

                elif formula[counter] is "(":
                    found_L_brac = True

                elif formula[counter] in "+" and not found_L_brac:

                    (node) = OrTree(build_tree(formula[:counter]), build_tree(
                        formula[counter + 1:]))
                    if (node.get_children())[0] is None or node.get_children()[1] is None:
                        node = None
                    connective_found = True
                elif formula[counter] in "*" and not found_L_brac:

                    (node) = AndTree(build_tree(formula[:counter]), build_tree(
                        formula[counter + 1:]))
                    if (node.get_children())[0] is None or node.get_children()[1] is None:
                        node = None
                    connective_found = True
                counter += 1

        elif len(formula) >= 2 and formula[0] is "-":
            if formula[1] not in "abcdefghijklmnopqrstuvwxyz-(":
                connective_found = True
                node = None
            else:
                node = NotTree(build_tree(formula[1:]))
                if (node.get_children())[0] is None:
                    node = None

        else:
            node = None
    return (node)


def draw_formula_tree(root):
    '''
    (FormulaTree) -> str
    This function returns the string representation of the
    formula tree given the root of the formula tree
    REQ: the root(which is a FormulaTree) is vale, thus,
    all of the left subtrees and right subtrees are valid
    DO EXAMPLES
    '''
    # Call helper function and return it's value
    string_rep = draw_tree_helper(root, 0)
    return string_rep


def draw_tree_helper(root, num_spaces):
    '''
    (FormulaTree, int) -> str
    This function returns the string representation of the formula
    given the root of the formula tree.
    This function is a helper function for draw_formula_tree.
    REQ: the root(which is a FormulaTree) is vale, thus,
    all of the left subtrees and right subtrees are valid
    '''
    # base case if the root is a leaf
    if isinstance(root, Leaf):
        str_rep = root.get_symbol()
        str_rep += "\n" + " " * (num_spaces)
    elif isinstance(root, NotTree):
        str_rep += draw_tree_helper((root.get_children())
                                    [0], num_spaces + 2)
    else:
        str_rep = root.get_symbol() + " "
        num_spaces += 2
        child_list = root.get_children()
        str_rep += ((draw_tree_helper(child_list[1], num_spaces)) + "\n" +
                    " " * num_spaces +
                    draw_tree_helper(child_list[0], num_spaces))

    return str_rep.rstrip()


def evaluate(root, variables, values):
    '''
    (FormulaTree, str, str) -> int
    REQ: len(variables) must equal len(values)
    REQ: values is a string which only contains 1's or 0's
    REQ: the leaf node's symbols must be in variable
    REQ: the root(which is a FormulaTree) is vale, thus,
    all of the left subtrees and right subtrees are valid
    >>> evaluate(build_tree("(a+b)"),"ab","10")
    1
    >>> evaluate(build_tree("(a*b)"),"ab",10)
    0
    >>> evaluate(build_tree("a"),'a','1')
    1
    >>> evaluate(build_tree("b"),'b','0')
    0
    >>> evaluate(build_tree("-(a+b)"),"ab","10")
    0
    >>> evaluate(build_tree("-(a*b)"),"ab",10)
    1
    >>> evaluate(build_tree((('a+b')*(-x+y))),"abxy","1010")
    0
    '''
    # base case if the root is a leaf
    if isinstance(root, Leaf):
        # get the roots variable and pass it to find_val function to find
        # it's value
        node_symbol = root.get_symbol()
        result = find_val(node_symbol, variables, values)
    else:
        # if the root is an OrTree or it is an AndTree
        if isinstance(root, OrTree) or isinstance(root, AndTree):
            # get the children of the root
            child_list = root.get_children()
            # traverse the left subtree and the right subtree recursively, untill
            #  we get the value of the left subtree and right subtree
            left_subtree = evaluate(child_list[0], variables, values)
            right_subtree = evaluate(child_list[1], variables, values)
            # if the root was an OrTree, get the larger of the right subtree
            # and left subtree (by definition of Or) to get the result.
            if isinstance(root, OrTree):
                result = max(left_subtree, right_subtree)
            else:
                # otherwise the root is an AndTree, so multiply the results of the
                # left subtree and right subtree to get the result
                result = left_subtree * right_subtree
        # otherwise the root is an NotTree
        else:
            # get the children
            child_list = root.get_children()
            # traverse the subtree recersively until we get the  result
            # of the subtree
            subtree = evaluate(child_list[0], variables, values)
            # get the result by sub doing 1 - the result of the subtree( by defenition of Not)
            result = 1 - subtree
    return result


def find_val(node_symbol, variables, values):
    '''
    (str, str, str) -> int
    This function findes the node node_symbol in variables
    and finds its co-responding value in values
    REQ: len(variables) must equal len(values)
    REQ: values is a string which only contains 1's or 0's
    '''
    found_variable = False
    pos = 0
    val = None
    # loop through all of the variables in the string
    while not found_variable:
        # check if the variable at the current position matches the
        # symbol of the node
        if variables[pos] == node_symbol:
            # set val equal to the co-responding value in values
            val = int(values[pos])
            found_variable = True
        pos += 1
    return val


def play2win_helper(root, variables, values):
    # base case if the root is a leaf
    if isinstance(root, Leaf):
        # get the roots variable and pass it to find_val function to find
        # it's value
        node_symbol = root.get_symbol()
        result = find_val(node_symbol, variables, values)
    else:
        # if the root is an OrTree or it is an AndTree
        if isinstance(root, OrTree) or isinstance(root, AndTree):
            # get the children of the root
            child_list = root.get_children()
            # traverse the left subtree and the right subtree recursively, untill
            #  we get the value of the left subtree and right subtree
            left_subtree = evaluate(child_list[0], variables, values)
            right_subtree = evaluate(child_list[1], variables, values)
            # if the root was an OrTree, get the larger of the right subtree
            # and left subtree (by definition of Or) to get the result.
            if isinstance(root, OrTree):
                result = max(left_subtree, right_subtree)
            else:
                # otherwise the root is an AndTree, so multiply the results of the
                # left subtree and right subtree to get the result
                result = left_subtree * right_subtree
        # otherwise the root is an NotTree
        else:
            # get the children
            child_list = root.get_children()
            # traverse the subtree recersively until we get the  result
            # of the subtree
            subtree = evaluate(child_list[0], variables, values)
            # get the result by sub doing 1 - the result of the subtree( by defenition of Not)
            result = 1 - subtree
    return result

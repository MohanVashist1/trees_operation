"""
Name: Mohan Vasnist
Student Number: 1004260514
UTorid: vashistm
# Copyright Nick Cheng, 2016, 2018
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2018
#
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

# Do not change this import statement, or add any of your own!
from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree

# Do not change any of the class declarations above this comment.

# Add your functions here.


def build_tree(formula):
    '''
    (str) -> FormulaTree
    This formula takes in a string representation of a fromula
    and returns the root of the formula (which will be a FormulaTree
    and points to the rest of the fomrula), if the formula is not
    valid, this function will return None
    >>> build_tree("a")
    Leaf("a")
    >>> build_tree("(a+b)")
    OrTree(Leaf('a'), Leaf('b'))
    >>> build_tree("-(a*-b)")
    NotTree(AndTree(Leaf('a'), NotTree(Leaf('b'))))
    '''
    node = None
    # base case the length of the formula is one and it is a lower-case letter
    if len(formula) is 1 and formula in "abcdefghijklmnopqrstuvwxyz":
        node = Leaf(formula)

    else:
        # recurssive case, check if the formula begins with a bracket and
        # ends with a bracket
        if len(formula) > 1 and formula[0] == "(" and formula[-1] == ")":
            # call the find_root function to get the root and it's subtrees
            node = find_root(formula, node)
        # second recurssive case where the formula begins with a not
        elif len(formula) >= 2 and formula[0] is "-":
            # check if the next character is a valid option to come after a not
            if formula[1] in "abcdefghijklmnopqrstuvwxyz-(":
                node = NotTree(build_tree(formula[1:]))
                if (node.get_children())[0] is None:
                    node = None
    return (node)


def find_root(formula, node):
    '''
    (str, FormulaTree) -> FromulaTree
    this function returns the root of formula
    (which will be a FormulaTree) and if the formula
    tree root has a left and right subtree, set the root's
    appropriate left and right subtree to their respected FormulaTree's.
    If the formula is invalid, return none.
    >>> find_root("(a+b)", None)
    OrTree(Leaf('a'), Leaf('b'))
    >>> find_root('((a+b)*c)', None)
    AndTree(OrTree(Leaf('a'), Leaf('b')), Leaf('c'))
    '''
    # take off the extrenous paranthesis around the formula
    formula = formula[1:-1]
    connective_found = False
    counter = 0
    root_found = False
    l_brac = 0
    r_brac = 0
    # loop thorugh until we have found the root or until we have reached
    # the end of the formula
    while not connective_found and counter < len(formula):
        # check if the formula at the index is a closing bracket
        if formula[counter] is ")":
            r_brac += 1
            # check if the number of left and right brackets match
            if l_brac - r_brac == 0:
                root_found = True
            else:
                root_found = False
        # check if the formula at the index is an opening bracket
        elif formula[counter] is "(":
            l_brac += 1
        # check if the formula at the index is an connective and the number
        # of opening and closing bracets match
        elif formula[counter] in "+*" and root_found:
            # check if the connective is a "+"
            if formula[counter] is "+":
                # set the root equal OrTree and set the left subtree equal
                # to the root of what came to the left of the connective.
                # set the right subtree equal to the root after the connective
                (node) = (OrTree(build_tree(formula[:counter]),
                                 build_tree(formula[counter + 1:])))
            # otherwise the root is an AndTree
            else:
                # set the root equal AndTree and set the left subtree equal
                # to the root of what came to the left of the connective.
                # set the right subtree equal to the root after the connective
                (node) = (AndTree(build_tree(formula[:counter]),
                                  build_tree(formula[counter + 1:])))
            # check if any of the root's subtrees are none, if they are,
            # set the node equal to none
            if ((node.get_children())[0] is None or
                    node.get_children()[1] is None):
                node = None
            connective_found = True
        # check if there was no opening and closing brackets at the first
        # index, then, the root will not be enclosed by brackets, e.g
        # (a+b) becomes a+b, since the extraneous parenthesis are
        # removed, so the connective does not have any brackets surrouding it.
        elif counter == 0 and l_brac == 0 and r_brac == 0:
            root_found = True
        counter += 1
    return node


def draw_formula_tree(root):
    '''
    (FormulaTree) -> str
    This function returns the string representation of the
    formula tree given the root of the formula tree
    REQ: the root(which is a FormulaTree) is vale, thus,
    all of the left subtrees and right subtrees are valid
    DO EXAMPLES
    >>> draw_formula_tree(OrTree(Leaf("a"),Leaf("b")))
    "+ b\n  a"
    >>> draw_formula_tree((AndTree(Leaf('a'), OrTree(Leaf('b'), Leaf('c')))))
    ("* + c\n    b\n  a")
    '''
    # Call helper function and return it's value
    str_rep = draw_tree_helper(root, 0)
    return str_rep


def draw_tree_helper(root, num_spaces):
    '''
    (FormulaTree, int) -> str
    This function returns the string representation of the formula
    given the root of the formula tree.
    This function is a helper function for draw_formula_tree.
    REQ: the root(which is a FormulaTree) is vale, thus,
    all of the left subtrees and right subtrees are valid
    >>> draw_formula_tree(OrTree(Leaf("a"),Leaf("b")),0)
    ("+ b\n  a")
    >>> draw_formula_tree((AndTree(Leaf('a'), OrTree(Leaf('b'), Leaf('c')))),0)
    ("* + c\n    b\n  a")
    '''
    str_rep = root.get_symbol() + " "
    # base case if the root is a leaf
    if isinstance(root, Leaf):
        str_rep += "\n" + " " * (num_spaces)
    # first recusive case where the root is a NotTree
    elif isinstance(root, NotTree):
        # traverse the child and add two spaces to it
        str_rep += draw_tree_helper((root.get_children())
                                    [0], num_spaces + 2)
    # otherwise the root is a AndTree of an OrTree
    else:
        # add two spaces to the total number of spaces
        num_spaces += 2
        # get the children of the root
        child_list = root.get_children()
        # traverse the right child and left child, then add a new line to
        # the end of the right child and then add the left child
        str_rep += ((draw_tree_helper(child_list[1], num_spaces)) + "\n" +
                    " " * num_spaces +
                    draw_tree_helper(child_list[0], num_spaces))
    # strip any extra spaces and lines and return
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


def play2win(root, turns, variables, values):
    if len(variables) == (len(values) + 1) or isinstance(root, Leaf) and values != '':
        result_0 = evaluate(root, variables, (values + "0"))
        result_1 = evaluate(root, variables, (values + '1'))
        if turns[-1] is "A":
            if result_0 == 0:
                best_move = 0
            elif result_1 == 0 and result_0 != 0:
                best_move = 1
            else:
                best_move = 0
        elif turns[-1] is "E":
            if result_1 == 1:
                best_move = 1
            elif result_0 == 1 and result_1 != 1:
                best_move = 0
            else:
                best_move = 1
    else:
        next_turn_var = variables[len(values)]
        next_turn_player = turns[len(values)]
        best_move = play2win_helper(
            root, turns, variables, values, next_turn_var, next_turn_player, None)
        temp = 1 - best_move
        values_temp = values + str(temp)
        values += str(best_move)
        for i in range(len(variables) - len(values)):
            values += str(play2win(root, turns, variables, values))
            values_temp += str(play2win(root, turns, variables, values_temp))
        check_if_win = evaluate(root, variables, values)
        check_if_win_temp = evaluate(root, variables, values_temp)
        if next_turn_player == "A" and check_if_win_temp == 0 and best_move != 0:
            best_move = 0
        elif next_turn_player == "E" and check_if_win_temp == 1 and best_move != 1:
            best_move = 1
            print("entered1")
        elif next_turn_player == "A" and check_if_win == 1 and best_move != 0:
            best_move = 0
        elif next_turn_player == "E" and check_if_win == 0 and best_move != 1:
            best_move = 1
            print("entered2")
    return best_move


def play2win_helper(root, turns, variables, values, next_turn_var, next_turn_player, best_move):
    if isinstance(root, AndTree) or isinstance(root, OrTree):
        child_list = root.get_children()
        if isinstance(child_list[0], Leaf) or isinstance(child_list[1], Leaf):
            if isinstance(child_list[0], Leaf) and child_list[0].get_symbol() == next_turn_var:
                if next_turn_player == "A":
                    best_move = 0
                else:
                    best_move = 1
            else:
                if child_list[1].get_symbol() == next_turn_var:
                    if next_turn_player == "A":
                        best_move = 0
                    else:
                        best_move = 1
                else:
                    best_move = None
    elif isinstance(root, NotTree):
        child_list = root.get_children()
        if isinstance(child_list[0], Leaf):
            if next_turn_player == "A":
                best_move = 1
            else:
                best_move = 0
        else:
            best_move = play2win_helper(root.get_children(
            )[0], turns, variables, values, next_turn_var, next_turn_player, best_move)
    if best_move is None:
        if not isinstance(root, Leaf):
            best_move = play2win_helper(root.get_children(
            )[0], turns, variables, values, next_turn_var, next_turn_player, best_move)
            if best_move is None:
                best_move = play2win_helper(root.get_children(
                )[1], turns, variables, values, next_turn_var, next_turn_player, best_move)
    return best_move


print(play2win(OrTree(NotTree(Leaf('x')), OrTree(
    NotTree(Leaf('y')), Leaf('z'))), 'EEA', 'xyz', ''))

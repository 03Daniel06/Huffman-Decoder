
"""
    File: huffman.py
    Author: Daniel Northcott
    Purpose: This program takes in two tree traversals inside of a file,
        a preorder and an inorder traversal of a tree. The program uses an
        algorithm to decode the tree. The tree is built then using huffman
        encoding we can find the paths of all the root to child paths in bits.
        moving left of the root implies a 0 and right implies a one. This path
        is then used inside the third line which is coded. The paths are then
        used to decode the message. The post order traversal is than printed.
"""

class BinaryTree:
    """ This class represents a binary tree

    This class defines a binary tree for huffman encoding
    """
    def __init__ (self, value):
        self._value = value
        self._left = None
        self._right = None
    
    def value(self):
        """ Returns the value of the node

        :parameter: self; the self object
        :return: value; an integer in our case
        """
        return self._value
    
    def left(self):
        """ Returns the left subtree to the node of the tree being passed in.

        :parameter: self; self object
        :return: binary tree; left subtree of node
        """
        return self._left
    
    def right(self):
        """ Returns the right subtree to the node of the tree being passed in.

        :parameter: self; self object
        :return: binary tree; right subtree of node
        """
        return self._right
    
    def insert_right(self, value):
        """ Inserts a node into the right child

        :parameter: value; the value to be passed into the new node
        :return: none
        """
        if self._right == None:
            self._right = BinaryTree(value)
        else:
            tree = BinaryTree(value)
            tree.right = self._right
            self._right = tree

    def insert_left(self, value):
        """ Inserts a node into the left child

        :parameter: value; the value to be passed into the new node
        :return: none
        """
        if self._left == None:
            self._left = BinaryTree(value)
        else:
            tree = BinaryTree(value)
            tree.right = self._left
            self._right = tree

    def is_leaf(self):
        """ Returns true if the current node is a leaf

        :return: True; if the node doesnt have a left and right tree; False,
            otherwise
        """
        if self._right is None and self._left is None:
            return True
        else:
            return False
        
def build_tree(preorder, inorder, start, end):
    """ Builds a tree given the preorder, and inorder traversal, with the
        start and end lengths given.

    :param preorder: string; the preorder traversal of the binary tree
    :param inorder: string; the inorder traversal of the binary tree
    :param start: int; 0 because the start is always 0
    :param end: the end index or length of the tree
    :return: The built tree from the given traversals
    """
    if start > end:
        return None
    
    in_root = preorder[0]
    in_root_index = inorder.index(in_root)

    new_root = BinaryTree(in_root)

    preorder.pop(0)

    new_root._left = build_tree(preorder,inorder, start, in_root_index -1)
    new_root._right = build_tree(preorder, inorder, in_root_index + 1, end)

    return new_root
        

    
def find_leaves(bt, list, path):
    """ Finds the leaf's and appends their huffman path into a list

    :param bt: binary tree; using to traverse
    :param list: a list of the leafs being passed in
    :param path: a refrence to a list that will contain all of the root to node
    paths
    :return: none; the path refrence is being modified
    """
    if bt is None:
        return
    elif bt.is_leaf():
        list.append(bt.value())
        list.append(path)
    else:
        find_leaves(bt.left(),list,(path+ "0"))
        find_leaves(bt.right(),list,path + '1')
        

def print_preorder(binaryTree):
    """ Prints the preorder traversal of the binary tree being passed in

    :param binaryTree: ADT of a binary tree
    :return: none
    """
    if binaryTree is None:
        return
    else:
        print(binaryTree.value())
        print_preorder(binaryTree.left())
        print_preorder(binaryTree.right())

def print_inorder(binaryTree):
    """ Prints the inorder traversal of the binary tree being passed in

    :param binaryTree: ADT of a binary tree
    :return: none
    """
    if binaryTree is None:
        return
    print_inorder(binaryTree.left())
    print(binaryTree.value())
    print_inorder(binaryTree.right())

def print_postorder(binaryTree,list):
    """ Prints the postorder traversal of the binary tree being passed in

    :param binaryTree: ADT of a binary tree
    :return: none
    """
    if binaryTree is None:
        return
    print_postorder(binaryTree.left(),list)
    print_postorder(binaryTree.right(),list)
    list.append(binaryTree.value())


def decode(paths, code, current_path = ""):
    """ Decodes the given string with the paths of the root to leaf
        node provided.

    :param paths: List; of the paths of root to leaf nodes
    :param code: String; string of the encoded message
    :param current_path: String; used to compare with the given paths
    :return: String; of the decoded message
    """
    none = ""
    if code == '':
        return none

    next_bit = code[0]
    remaining_code = code[1:]

    for value, path in paths:
        if path.startswith(current_path + next_bit):
            if len(path) == len(current_path) + 1:
                return value + decode(paths, remaining_code)
            else:
                return decode(paths, remaining_code, current_path +
                                      next_bit)

    return none



def main():
    filename = str(input('Input file: '))
    file = open(filename, 'r')
    
    preorder = str(file.readline()).strip('\n').split()
    inorder = str(file.readline()).strip('\n').split()


    code = str(file.readline())
    file.close()
    leafs = []

    bt = build_tree(preorder,inorder,0,len(inorder)-1)
    path = ''
    find_leaves(bt, leafs, path)
    paths = []

    for i in range(0, len(leafs), 2):
        if i + 1 < len(leafs):
            paths.append([leafs[i], leafs[i + 1]])
    temp = ''
    value = decode(paths,code, temp)
    postord = []
    print_postorder(bt,postord)
    postord_s = ''
    for i in postord:
        postord_s += i + " "
    postord_s.rstrip()

    print(postord_s)
    print(value)





if __name__ == '__main__':
    main()
    

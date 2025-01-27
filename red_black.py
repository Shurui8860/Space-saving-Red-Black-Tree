# File:     red_black.py
# Author:   John Longley
# Date:     October 2022

# Template file for Inf2-IADS (2022-23) Coursework 1, Part B
# Implementation of dictionaries by red-black trees: space-saving version

# Provided code:

Red, Black = True, False


def colourStr(c):
    return 'R' if c == Red else 'B'


Left, Right = 0, 1


def opposite(branch):
    return 1 - branch


branchLabels = ['l', 'r']


class Node():

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.colour = Red
        self.left = None
        self.right = None

    def getChild(self, branch):
        if branch == Left:
            return self.left
        else:
            return self.right

    def setChild(self, branch, y):
        if branch == Left:
            self.left = y
        else:
            self.right = y

    def __repr__(self):
        return str(self.key) + ':' + str(self.value) + ':' + colourStr(self.colour)

    def search(self, key):
        if self.key == key:
            return self.value
        elif self.key > key and self.left is not None:
            return self.left.search(key)
        elif self.key < key and self.right is not None:
            return self.right.search(key)
        else:
            return None


# Use None for all trivial leaf nodes

def colourOf(x):
    if x is None:
        return Black
    else:
        return x.colour


class RedBlackTree():

    def __init__(self):
        self.root = None
        self.stack = []

    # TODO: Task 1.
    #   lookup(self,key)
    def lookup(self, key):
        return self.root.search(key)

    # TODO: Task 2.
    #   plainInsert(self,key,value)

    # The following method inserts a new key-value pair into the ordered tree at the correct position,
    # without worrying about colour information or the rules specific to red-black trees.
    def plainInsert(self, key, value):

        parentNode = None
        currentNode = self.root
        # trace down a simple path downward looking for a Nil to replace with the input
        # or a node with the given key to update its value.
        while currentNode is not None:
            parentNode = currentNode
            if key < currentNode.key:
                currentNode = currentNode.left
                # update the path in the stack
                self.stack.append(parentNode)
                self.stack.append(Left)
            elif key > currentNode.key:
                currentNode = currentNode.right
                self.stack.append(parentNode)
                self.stack.append(Right)
            elif key == currentNode.key:
                break

        newNode = Node(key, value)

        # case one: the tree is initially empty.
        if parentNode is None:
            self.root = newNode
        # case two: the given key is already present in the tree, just overwrite the value.
        elif key == parentNode.key:
            currentNode.value = value        # update the value of the node
            self.stack.append(currentNode)
            return
        # case three: the tree is not empty, and key is not in the tree.
        elif key < parentNode.key:
            parentNode.left = newNode        # the new node replaces the nil.
        elif key > parentNode.key:
            parentNode.right = newNode

        self.stack.append(newNode)

    # TODO: Task 3.
    #   tryRedUncle(self)
    #   repeatRedUncle(self):

    # Try to apply the red-uncle rule, and return true if the red-uncle rule has been applied.
    def tryRedUncle(self):
        # If the new node has no grandparent, the red-uncle rule is not applicable.
        if len(self.stack) < 5:
            return False
        [child, dp, parent, dpp] = [self.stack.pop() for _ in range(4)]
        grandparent = self.stack[-1]
        uncle = grandparent.getChild(opposite(dpp))
        # check the conditions for the red-uncle rule.
        if colourOf(parent) == Red and colourOf(uncle) == Red and colourOf(child) == Red:
            parent.colour = Black
            uncle.colour = Black
            grandparent.colour = Red
            return True
        else:
            # restore the popped values in the stack.
            for elem in [dpp, parent, dp, child]:
                self.stack.append(elem)
            return False

    # apply the red-uncle rule if possible
    def repeatRedUncle(self):
        repeat = True
        while repeat:
            repeat = self.tryRedUncle()

    # Provided code to support Task 4:
    def toNextBlackLevel(self, node):
        # inspect subtree down to the next level of blacks
        # and return list of components (subtrees or nodes) in L-to-R order
        # (in cases of interest there will be 7 components A,a,B,b,C,c,D).
        if colourOf(node.left) == Black:  # node.left may be None
            leftHalf = [node.left]
        else:
            leftHalf = self.toNextBlackLevel(node.left)
        if colourOf(node.right) == Black:
            rightHalf = [node.right]
        else:
            rightHalf = self.toNextBlackLevel(node.right)
        return leftHalf + [node] + rightHalf


    def balancedTree(self, comps):
        # build a new (balanced) subtree from list of 7 components
        [A, a, B, b, C, c, D] = comps
        a.colour = Red
        a.left = A
        a.right = B
        c.colour = Red
        c.left = C
        c.right = D
        b.colour = Black
        b.left = a
        b.right = c
        return b

    # TODO: Task 4.
    #   endgame(self)
    #   insert(self,key,value)

    def endgame(self):
        # case one: the root is Red
        if self.root.colour == Red:
            self.root.colour = Black

        # If the length of the stack is less than three, then there are no parent of the node,
        # which means the input key equals the key of root. In this case, no additional operations are required.
        elif len(self.stack) >= 3:
            [child, _, parent] = [self.stack.pop() for _ in range(3)]

            # case two: red parent, red child, and black uncle, endgame scenario.
            if colourOf(parent) == Red and colourOf(child) == Red:
                [_, grandparent] = [self.stack.pop() for _ in range(2)]
                comps = self.toNextBlackLevel(grandparent)
                centralNode = self.balancedTree(comps)

                # connect the subtree to the main RB tree.
                if grandparent == self.root:
                    self.root = centralNode
                else:
                    [dppp, grandgrandparent] = [self.stack.pop() for _ in range(2)]
                    grandgrandparent.setChild(dppp, centralNode)
        return

    # inserting the given key-value pair into the tree and performing all necessary fix-up.
    def insert(self, key, value):
        self.plainInsert(key, value)
        self.repeatRedUncle()
        self.endgame()
        self.stack.clear()

    # Provided code:

    # Printing tree contents

    def __str__(self, x):
        if x == None:
            return 'None:B'
        else:
            leftStr = '[ ' + self.__str__(x.left) + ' ] '
            rightStr = ' [ ' + self.__str__(x.right) + ' ]'
            return leftStr + x.__str__() + rightStr

    def __repr__(self):
        return self.__str__(self.root)

    def showStack(self):
        return [x.__str__() if isinstance(x, Node) else branchLabels[x]
                for x in self.stack]

    # All keys by left-to-right traversal

    def keysLtoR_(self, x):
        if x == None:
            return []
        else:
            return self.keysLtoR_(x.left) + [x.key] + self.keysLtoR_(x.right)

    def keysLtoR(self):
        return self.keysLtoR_(self.root)


# End of class RedBlackTree


# Creating a tree by hand:

sampleTree = RedBlackTree()
sampleTree.root = Node(2, 'two')
sampleTree.root.colour = Black
sampleTree.root.left = Node(1, 'one')
sampleTree.root.left.colour = Black
sampleTree.root.right = Node(4, 'four')
sampleTree.root.right.colour = Red
sampleTree.root.right.left = Node(3, 'three')
sampleTree.root.right.left.colour = Black
sampleTree.root.right.right = Node(6, 'six')
sampleTree.root.right.right.colour = Black


# For fun: sorting algorithm using trees
# Will remove duplicates

def TreeSort(L):
    T = RedBlackTree()
    for x in L:
        T.insert(x, None)
    return T.keysLtoR()

# End of file

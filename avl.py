import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)

class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # Implement the add method
    def add(self, value: object) -> None:
        # Check if the value already exists in the tree to avoid duplicates
        if self.contains(value):
            return
        self._root = self._add_recursive(self._root, value)  # Begin the recursive process to insert the new value into the tree
        self._root.parent = None 

    def _add_recursive(self, node, value):

        # If the current node is None, create and return a new AVLNode with the given value
        if node is None:
            return AVLNode(value)
        elif value < node.value:

        # If the value is less than the current node's value, recurse left
            node.left = self._add_recursive(node.left, value)
            node.left.parent = node
        elif value > node.value:
            node.right = self._add_recursive(node.right, value)
            node.right.parent = node

        # After insertion, update the current node's height
        self._update_height(node)
        return self._rebalance(node)

    # Implement the remove method
    def remove(self, value: object) -> bool:

        # Check if the value exists in the tree
        if self.contains(value):
            self._root = self._remove_recursive(self._root, value)
            # Begin the recursive process to remove the value from the tree
            if self._root:
                self._root.parent = None 
            return True # Indicate the value was successfully removed
        return False

    def _remove_recursive(self, node, value):
         # If the current node is None, simply return it (base case)
        if not node:
            return node

        if value < node.value:
            node.left = self._remove_recursive(node.left, value)
        elif value > node.value:
            node.right = self._remove_recursive(node.right, value)
        else:
            # If the current node is the node to remove
            if not node.left:
                temp = node.right
                node = None
                return temp
            elif not node.right:
                temp = node.left
                node = None
                return temp
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._remove_recursive(node.right, temp.value)

        if node is None:  # If the node has been removed, return None
            return node

        # Update the height of the ancestor node
        self._update_height(node)
        
        # Rebalance the tree starting from the current node, and return the (possibly) new node
        return self._rebalance(node)

    # Helper methods for AVL rotations and balancing
    def _rotate_left(self, z):
        y = z.right  # Set y as z's right child
        T2 = y.left  
        y.left = z  # Move z to y's left
        z.right = T2  

        # We update parent pointer
        if T2:
            T2.parent = z
        y.parent = z.parent
        z.parent = y
        if T2:
            T2.parent = z

    # If y is now the root or a subtree, update the parent's child pointer
        if y.parent and y.parent.left == z:
            y.parent.left = y
        elif y.parent:
            y.parent.right = y

    # Update heights of z and y after rotation
        self._update_height(z)
        self._update_height(y)
        return y

    # perform right rotation on the node 'z'
    def _rotate_right(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        if T3:
            T3.parent = z
        y.parent = z.parent
        z.parent = y
        if T3:
            T3.parent = z

    # If y is now the root or a subtree, update the parent's child pointer
        if y.parent and y.parent.right == z:
            y.parent.right = y
        elif y.parent:
            y.parent.left = y

        self._update_height(z)
        self._update_height(y)
        return y  # Return the new root of the subtree

    def _rebalance(self, node):
        balance = self._get_balance(node)

      # Check for left-right case and perform left rotation on left child first
        if balance > 1:
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

    #Right heavy subtree
        if balance < -1:
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    #Updates the height of a node based on the heights of its children.
    def _update_height(self, node):
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
    
    #Returns the height of a node. If the node is None, returns -1.
    def _get_height(self, node):
        if not node:
            return -1
        return node.height

    # Computes the balance factor of a node as the difference in heights between its left and right subtrees.
    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    #Finds the node with the minimum value in a subtree rooted with the given node.
    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

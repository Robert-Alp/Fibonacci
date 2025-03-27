class Node:

    def __init__(self, value, next: 'Node'):
        self.value = value
        self.next = next


    def addValue(self, value: int, node: 'Node'):
        if node.next == None:
            node.next = Node(value, None)
            return
        self.addValue(value, node.next)
        

    def show(self, node: 'Node') -> None:
        if node.next == None:
            print(f"{node.value} -> X")
            return None
        print(f"{node.value} -> ", end="")
        return self.show(node.next)
    

    def remove(self, value, node: 'Node'):
        if node is None:
            return None
        if node.value == value:
            return node.next 
        node.next = self.remove(value, node.next) 
        return node
    

        

# node = Node(4, None)


# node.addValue(5, node)
# node.addValue(1, node)
# node.addValue(2, node)
# node.addValue(3, node)
# node.addValue(7, node)
# node.addValue(9, node)



# node.show(node)

# node.remove(2, node)
# node.remove(2, node)

# node.show(node)


class BinaryTree:

    def __init__(self, gauche: 'BinaryTree', droite: 'BinaryTree', value: int):
        self.gauche = gauche
        self.droite = droite
        self.value = value






def show( binaryTree: 'BinaryTree'):
    if binaryTree == None:
        return 
    show(binaryTree.gauche) 
    show(binaryTree.droite) 
    print(binaryTree.value)





binaryTree30 = BinaryTree(BinaryTree(BinaryTree(None, None, 15), BinaryTree(None, None, 25),20), BinaryTree(None, None, 35), 30)

binaryTree70 = BinaryTree(BinaryTree(BinaryTree(BinaryTree(None, None, 45), None, 50), None, 60), BinaryTree(None, None, 80), 70)


binaryTree40 = BinaryTree(binaryTree30, binaryTree70, 40)


show(binaryTree40)

    
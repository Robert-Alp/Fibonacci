class BinaryTree:

    def __init__(self, gauche: 'BinaryTree', droite: 'BinaryTree', value: int):
        self.gauche = gauche
        self.droite = droite
        self.value = value


def prefixe( binaryTree: 'BinaryTree'):
    if binaryTree == None:
        return 
    print(binaryTree.value)
    prefixe(binaryTree.gauche) 
    prefixe(binaryTree.droite) 

def infixe( binaryTree: 'BinaryTree'):
    if binaryTree == None:
        return 
    infixe(binaryTree.gauche) 
    print(binaryTree.value)
    infixe(binaryTree.droite) 

def sufixe( binaryTree: 'BinaryTree'):
    if binaryTree == None:
        return 
    sufixe(binaryTree.gauche) 
    sufixe(binaryTree.droite) 
    print(binaryTree.value)

def search(value, binaryTree: 'BinaryTree') -> bool:
    if binaryTree is None:
        return False
    elif binaryTree.value == value:
        return True
 
    return search(value, binaryTree.gauche) or search(value, binaryTree.droite)

def height(node):
    if (node == None) :
        return -1
    return 1 + max(height(node.gauche), height(node.droite))
    


binaryTree30 = BinaryTree(BinaryTree(BinaryTree(None, None, 15), BinaryTree(None, None, 25),20), BinaryTree(None, None, 35), 30)

binaryTree70 = BinaryTree(BinaryTree(BinaryTree(BinaryTree(None, None, 45), None, 50), None, 60), BinaryTree(None, None, 80), 70)

binaryTree40 = BinaryTree(binaryTree30, binaryTree70, 40)


print(search(45, binaryTree40))

print(height(binaryTree40))
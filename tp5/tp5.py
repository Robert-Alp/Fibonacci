class BinaryTree:

    def __init__(self, gauche: 'BinaryTree', droite: 'BinaryTree', value: int):
        self.gauche = gauche
        self.droite = droite
        self.value = value

    def __str__(self):
        return f"({self.gauche},{self.value},{self.droite})"
    

def frequence(text):
    dict = {}
    for lettre in text:
        if lettre not in dict:
            dict[lettre] = 1
        else:
            dict[lettre] += 1
    return dict


def bubbleSort(dict):
    tab = list(dict.keys())
    size = len(tab)
    for i in range(size - 1):
        for j in range(size - i):
            if j < size and j + 1 < size:
                if dict[tab[j]] > dict[tab[j + 1]]:
                    max = tab[j]
                    min = tab[j + 1]
                    tab[j] = min
                    tab[j + 1] = max
    return tab


def arbre(tab, dict):
    if len(tab) < 2:
        return None
    
    tabCopy = tab.copy()
    print(tabCopy)
    nodes = []

    while len(tabCopy) > 0:
        if len(tabCopy) > 2:
            gauche = tabCopy.pop(0)
            droite = tabCopy.pop(0)
            nodes.append(BinaryTree(BinaryTree(None, None, gauche), BinaryTree(None, None, droite), dict[gauche] + dict[droite]))
        if  len(tabCopy) == 1:
            lastElement = tabCopy.pop(0)
            nodes.append(BinaryTree(None, None, lastElement))

    while len(nodes) > 1:
        if len(nodes) >= 2:
            one = nodes.pop(0)
            two = nodes.pop(0)
            valueOne =  one.value if str(one.value).isdigit() else dict[one.value]
            valueTwo =   two.value if str(two.value).isdigit() else dict[two.value]
            currentTree = BinaryTree(one, two, valueOne + valueTwo)
            nodes.insert(0, currentTree)

    return nodes[0]
    
def encode(tree: 'BinaryTree', code: str, dict):
    if tree == None:
        return None
    if not str(tree.value).isdigit():
        dict[tree.value] = code
        return True
    encode(tree.gauche, code + "0", dict)
    encode(tree.droite, code + "1", dict)


tabFrenquence = frequence("travaille")
tableSorte = bubbleSort(tabFrenquence)

tree = arbre(tableSorte, tabFrenquence)

print(tree)

dictCode = {}
print(encode(tree, "", dictCode))
print(dictCode)
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

def compresser(texte: str):

    tabFrenquence = frequence(texte)
    tableSorte = bubbleSort(tabFrenquence)

    tree = arbre(tableSorte, tabFrenquence)

    dictCode = {}
    encode(tree, "", dictCode)
    code = ""
    for lettre in texte:
        code += dictCode[lettre]

    return (code, dictCode, tree)

def decomprimer(tree: 'BinaryTree', code):
    if tree == None or len(code) == 0:
        return ""
    if tree.gauche == None and tree.droite == None:
        return tree.value
    if code[0] == "0":
        return decomprimer(tree.gauche, code[1:]) + decomprimer(tree.droite, code[1:])
    if code[0] == "1":
        return decomprimer(tree.droite, code[1:]) + decomprimer(tree.gauche, code[1:])


code_binaire, dictionnaire, Tree = compresser("travaille")

print("Code binaire", code_binaire)
print("Dictionnaire", dictionnaire)
print("Arbre", Tree)

print("Decomprimer", decomprimer(Tree, code_binaire))

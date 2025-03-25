

tab = [1, 3, 6, 2, 9, 0]

def min(tab):
    minVal = tab[0]
    for i in tab:
        if i < minVal:
            return i
    return minVal

print(min(tab))
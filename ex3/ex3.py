#Bubble sort
tab =  [60, 9, 50, 3, 5]

def bubble(tab):
    size = len(tab)

    for i in range(size - 1):
        for j in range(size - 1):
            k = i + j
            if k < size and k + 1 < size:
                if tab[k] > tab[k + 1]:
                    max = tab[k]
                    min = tab[k + 1]
                    tab[k] = min
                    tab[k + 1] = max
    return tab

print(bubble(tab))

#Selection Sort


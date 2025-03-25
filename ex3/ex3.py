#Bubble sort
tab =  [60, 9, 50, 3, 5, 2]

print("Au début", tab)

def bubble(tab):
    size = len(tab)
    for i in range(size - 1):
        print("------------------")
        for j in range(size - i):
            # k = i + j
            print(j)
            if j < size and j + 1 < size:
                if tab[j] > tab[j + 1]:
                    max = tab[j]
                    min = tab[j + 1]
                    tab[j] = min
                    tab[j + 1] = max
    return tab

print("Bubble sort", bubble(tab))


#Selection Sort
def selection(tab):
    size = len(tab)

    l = None
    currentMin = None
    for i in range(size):
        for j in range(i + 1, size):
            if tab[j] < tab[i] and ((currentMin == None ) or (tab[j] < currentMin)):
                currentMin = tab[j]
                l = j
        if l != None:
            max = tab[i] 
            min = tab[l]
            tab[i] = min
            tab[l] = max
        l = None
        currentMin = None

    return tab

print("Selection sort", selection(tab))
# x = range(3, 6)
# print(list(x))


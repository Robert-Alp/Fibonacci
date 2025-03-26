import random

taille = 10  

tab = [random.randint(1, 100) for _ in range(taille)]

#Bubble sort
print("Au début", tab)

def bubble(tab):
    size = len(tab)
    for i in range(size - 1):
        for j in range(size - i):
            if j < size and j + 1 < size:
                if tab[j] > tab[j + 1]:
                    max = tab[j]
                    min = tab[j + 1]
                    tab[j] = min
                    tab[j + 1] = max
    return tab

print("Bubble sort: ", bubble(tab)) 


#Selection Sort
def selection(tab):
    size = len(tab)

    
    for i in range(size):
        # print(f"---------{i}----------")
        l = None
        currentMin = None
        for j in range(i + 1, size):
            # print(j)
            if ( (tab[j] < tab[i]) and ((currentMin == None ) or (tab[j] < currentMin)) ):
                currentMin = tab[j]
                l = j
        if l != None:
            max = tab[i] 
            min = tab[l]
            tab[i] = min
            tab[l] = max
 
    return tab


def instertion(tab):
    size =  len(tab)

    for i in range(size):
        for j in range(0, i):
            currentIndice = (i - 1) - j
            if currentIndice - 1 >= 0 :
                if currentIndice + 1 < size and tab[currentIndice + 1] < tab[currentIndice]:
                    min = tab[currentIndice] 
                    max = tab[currentIndice + 1]
                    tab[currentIndice] = max
                    tab[currentIndice + 1] = min

    return tab
            

# def partition(tab):
    

def quick(tab):
    
    size = len(tab)
    if size < 2:
        return tab
    
    
print("Selection sort: ", selection(tab))
print("Insertion sort: ", instertion(tab))



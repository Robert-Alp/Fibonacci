import time

def fibonacci_list(n):
    if n <= 0:
        return [0]
    elif n == 1:
        return [0, 1]
    
    fib_list = [0, 1]
    for i in range(2, n):
        fib_list.append(fib_list[i-1] + fib_list[i-2])
    return fib_list

def fibonacci_recursive(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

def measure_time(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result, end - start

n = int(input("Entrez un nombre pour générer la suite de Fibonacci : "))

# Génération de la suite dans différentes structures de données
fib_list, time_list = measure_time(fibonacci_list, n)
fib_tuple, time_tuple = measure_time(tuple, fib_list)
fib_set, time_set = measure_time(set, fib_list)
fib_dict, time_dict = measure_time(lambda x: {i: x[i] for i in range(len(x))}, fib_list)

# Mesure du temps d'accès séquentiel
start = time.perf_counter()
for i in range(n):
    _ = fib_list[i]
end = time.perf_counter()
time_access_list = end - start

start = time.perf_counter()
for i in range(n):
    _ = fib_tuple[i]
end = time.perf_counter()
time_access_tuple = end - start

start = time.perf_counter()
for num in fib_set:
    _ = num
end = time.perf_counter()
time_access_set = end - start

start = time.perf_counter()
for i in range(n):
    _ = fib_dict[i]
end = time.perf_counter()
time_access_dict = end - start

_, time_rec = measure_time(fibonacci_recursive, min(n, 30)) 

# Affichage des résultats
print(f"Temps de génération :\nList: {time_list:.6f}s\nTuple: {time_tuple:.6f}s\nSet: {time_set:.6f}s\nDict: {time_dict:.6f}s")
print(f"Temps d'accès :\nList: {time_access_list:.6f}s\nTuple: {time_access_tuple:.6f}s\nSet: {time_access_set:.6f}s\nDict: {time_access_dict:.6f}s")
print(f"Temps d'exécution récursif (n=30 max) : {time_rec:.6f}s")
import requests
import pymongo
import time
from typing import List, Dict, Callable

# Étape 1 : Récupération des données depuis l'API CoinGecko
def fetch_data_from_api() -> List[Dict]:
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Extraction de 5 champs pertinents
        return [{"name": coin["name"], "symbol": coin["symbol"], "current_price": coin["current_price"],
                 "market_cap": coin["market_cap"], "total_volume": coin["total_volume"]} for coin in data]
    else:
        raise Exception(f"Erreur API : {response.status_code}")

# Étape 2 : Stockage dans MongoDB
def store_in_mongodb(data: List[Dict]) -> List[Dict]:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["crypto_db"]
    collection = db["coins"]
    collection.drop()  # Réinitialiser la collection pour éviter les doublons
    result = collection.insert_many(data)
    print(f"Inserted {len(result.inserted_ids)} documents into MongoDB.")
    return list(collection.find({}, {"_id": 0}))  # Récupérer sans l'_id

# Étape 3 : Algorithmes de tri
def bubble_sort(data: List[Dict], key: str) -> List[Dict]:
    sorted_data = data.copy()
    n = len(sorted_data)
    for i in range(n-1):
        for j in range(n-i-1):
            if sorted_data[j][key] > sorted_data[j+1][key]:
                sorted_data[j], sorted_data[j+1] = sorted_data[j+1], sorted_data[j]
    return sorted_data

def selection_sort(data: List[Dict], key: str) -> List[Dict]:
    sorted_data = data.copy()
    n = len(sorted_data)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if sorted_data[j][key] < sorted_data[min_idx][key]:
                min_idx = j
        sorted_data[i], sorted_data[min_idx] = sorted_data[min_idx], sorted_data[i]
    return sorted_data

def insertion_sort(data: List[Dict], key: str) -> List[Dict]:
    sorted_data = data.copy()
    for i in range(1, len(sorted_data)):
        key_item = sorted_data[i]
        j = i - 1
        while j >= 0 and sorted_data[j][key] > key_item[key]:
            sorted_data[j + 1] = sorted_data[j]
            j -= 1
        sorted_data[j + 1] = key_item
    return sorted_data

def quick_sort(data: List[Dict], key: str) -> List[Dict]:
    if len(data) <= 1:
        return data
    sorted_data = data.copy()
    pivot = sorted_data[len(sorted_data) // 2][key]
    left = [x for x in sorted_data if x[key] < pivot]
    middle = [x for x in sorted_data if x[key] == pivot]
    right = [x for x in sorted_data if x[key] > pivot]
    return quick_sort(left, key) + middle + quick_sort(right, key)

# Mesure du temps d'exécution
def time_and_sort(data: List[Dict], key: str, sort_func: Callable) -> tuple:
    start = time.perf_counter()
    sorted_data = sort_func(data, key)
    end = time.perf_counter()
    return sorted_data, (end - start) * 1000  # Temps en millisecondes

# Bonus : Filtrage des données
def filter_data(data: List[Dict], key: str, operator: str, value: float) -> List[Dict]:
    if operator == ">":
        return [d for d in data if d[key] > value]
    elif operator == "<":
        return [d for d in data if d[key] < value]
    elif operator == "==":
        return [d for d in data if d[key] == value]
    return data

# Étape 4 : Programme principal
def main():
    # Récupération des données
    print("Récupération des données depuis l'API...")
    api_data = fetch_data_from_api()

    # Stockage dans MongoDB
    print("Stockage des données dans MongoDB...")
    data_from_db = store_in_mongodb(api_data)

    # Choix du critère de tri
    sort_keys = ["current_price", "market_cap", "total_volume"]
    print("Champs disponibles pour le tri :", sort_keys)
    while True:
        sort_key = input("Choisissez un critère de tri (par exemple, current_price, market_cap, total_volume) : ")
        if sort_key in sort_keys:
            break
        print("Critère invalide. Réessayez.")

    # Bonus : Filtrage optionnel
    use_filter = input("Voulez-vous filtrer les données avant le tri ? (oui/non) : ").lower() == "oui"
    if use_filter:
        print("Opérateurs disponibles : >, <, ==")
        filter_key = input(f"Choisissez un champ à filtrer ({sort_keys}) : ")
        operator = input("Choisissez un opérateur (> , < , ==) : ")
        value = float(input("Entrez une valeur numérique : "))
        data_from_db = filter_data(data_from_db, filter_key, operator, value)
        print(f"Nombre de données après filtrage : {len(data_from_db)}")

    # Test des algorithmes de tri
    sort_functions = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Quick Sort": quick_sort
    }
    results = {}
    for name, func in sort_functions.items():
        sorted_data, exec_time = time_and_sort(data_from_db, sort_key, func)
        results[name] = {"data": sorted_data, "time": exec_time}
        print(f"\n{name}: Time taken = {exec_time:.2f} ms")
        print("5 premières entrées triées :")
        for entry in sorted_data[:5]:
            print(f"  {entry['name']} - {sort_key}: {entry[sort_key]}")

    # Sélection de l'algorithme le plus rapide
    fastest = min(results, key=lambda x: results[x]["time"])
    print(f"\nL'algorithme le plus rapide est : {fastest} avec {results[fastest]['time']:.2f} ms")

if __name__ == "__main__":
    main()
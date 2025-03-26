import requests
import pymongo
import time
from typing import List, Dict, Optional

def fetch_data_from_api() -> List[Dict]:
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [{"name": coin["name"], "symbol": coin["symbol"], "current_price": coin["current_price"],
                 "market_cap": coin["market_cap"], "total_volume": coin["total_volume"]} for coin in data]
    else:
        raise Exception(f"Erreur API : {response.status_code}")

def store_in_mongodb(data: List[Dict]) -> List[Dict]:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["crypto_db"]
    collection = db["coins"]
    collection.drop() 
    result = collection.insert_many(data)
    print(f"Inserted {len(result.inserted_ids)} documents into MongoDB.")
    return list(collection.find({}, {"_id": 0})) 

def binary_search(data: List[Dict], key: str, target: float) -> Optional[int]:
    left, right = 0, len(data) - 1
    while left <= right:
        mid = (left + right) // 2
        if data[mid][key] == target:
            return mid
        elif data[mid][key] < target:
            left = mid + 1
        else:
            right = mid - 1
    return None

def linear_search(data: List[Dict], key: str, target: float) -> Optional[int]:
    for i, item in enumerate(data):
        if item[key] == target:
            return i
    return None

def quick_sort(data: List[Dict], key: str) -> List[Dict]:
    if len(data) <= 1:
        return data
    sorted_data = data.copy()
    pivot = sorted_data[len(sorted_data) // 2][key]
    left = [x for x in sorted_data if x[key] < pivot]
    middle = [x for x in sorted_data if x[key] == pivot]
    right = [x for x in sorted_data if x[key] > pivot]
    return quick_sort(left, key) + middle + quick_sort(right, key)

def measure_time(data: List[Dict], key: str, target: float, search_func: callable) -> tuple:
    start = time.perf_counter()
    result = search_func(data, key, target)
    end = time.perf_counter()
    return result, (end - start) * 1000 

def main():
    print("Récupération des données depuis l'API...")
    api_data = fetch_data_from_api()
    print("Stockage des données dans MongoDB...")
    data_from_db = store_in_mongodb(api_data)

    search_keys = ["current_price", "market_cap", "total_volume"]
    print("Champs disponibles pour la recherche :", search_keys)
    while True:
        search_key = input("Choisissez un critère de recherche (ex. current_price) : ")
        if search_key in search_keys:
            break
        print("Critère invalide. Réessayez.")

    print(f"Tri des données sur {search_key}...")
    sorted_data = quick_sort(data_from_db, search_key)

    while True:
        try:
            target = float(input(f"Entrez une valeur à rechercher pour {search_key} : "))
            break
        except ValueError:
            print("Veuillez entrer une valeur numérique.")

    binary_result, binary_time = measure_time(sorted_data, search_key, target, binary_search)
    if binary_result is not None:
        print(f"\nBinary Search : Élément trouvé à l'index {binary_result}")
        print(f"Détails : {sorted_data[binary_result]}")
    else:
        print("\nBinary Search : Élément non trouvé.")
    print(f"Temps d'exécution : {binary_time:.4f} ms")

    linear_result, linear_time = measure_time(sorted_data, search_key, target, linear_search)
    if linear_result is not None:
        print(f"\nLinear Search : Élément trouvé à l'index {linear_result}")
        print(f"Détails : {sorted_data[linear_result]}")
    else:
        print("\nLinear Search : Élément non trouvé.")
    print(f"Temps d'exécution : {linear_time:.4f} ms")

    print(f"\nAnalyse des performances :")
    print(f"Binary Search (O(log n)) : {binary_time:.4f} ms")
    print(f"Linear Search (O(n)) : {linear_time:.4f} ms")
    speedup = linear_time / binary_time if binary_time > 0 else float('inf')
    print(f"Binary Search est {speedup:.2f}x plus rapide que Linear Search.")

if __name__ == "__main__":
    main()
import time
import requests
import pymongo
import redis
import json

def fetch_data(api_url, keys):
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        filtered_data = [{key: item[key] for key in keys if key in item} for item in data]
        return filtered_data
    return []

def store_mongodb(data, db_name="apiSort", collection_name="data"):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    collection = db[collection_name]
    collection.insert_many(data)
    return collection.find()

def store_redis(data, redis_key="tp_data"):
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set(redis_key, json.dumps(data))
    return json.loads(r.get(redis_key))

def bubble_sort(data, key):
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j][key] > arr[j+1][key]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def selection_sort(data, key):
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j][key] < arr[min_idx][key]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(data, key):
    arr = data.copy()
    for i in range(1, len(arr)):
        key_value = arr[i]
        j = i - 1
        while j >= 0 and key_value[key] < arr[j][key]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_value
    return arr

def quick_sort(data, key):
    if len(data) <= 1:
        return data
    pivot = data[len(data) // 2]
    left = [x for x in data if x[key] < pivot[key]]
    middle = [x for x in data if x[key] == pivot[key]]
    right = [x for x in data if x[key] > pivot[key]]
    return quick_sort(left, key) + middle + quick_sort(right, key)

def measure_sorting_time(data, key):
    sorting_algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Quick Sort": quick_sort
    }
    times = {}
    for name, sort_func in sorting_algorithms.items():
        start_time = time.time()
        sorted_data = sort_func(data, key)
        end_time = time.time()
        times[name] = (end_time - start_time) * 1000
    return times

if __name__ == "__main__":
    api_url = "https://api.coincap.io/v2/assets"
    keys = ["id", "rank", "symbol", "name", "priceUsd"]
    data = fetch_data(api_url, keys)
    
    if data:
        print("Données récupérées avec succès")
        db_choice = input("Choisir le stockage (mongodb/redis) : ").strip().lower()
        
        if db_choice == "mongodb":
            stored_data = list(store_mongodb(data))
        elif db_choice == "redis":
            stored_data = store_redis(data)
        else:
            print("Choix invalide, stockage ignoré.")
            stored_data = data
        
        sort_key = "priceUsd"
        times = measure_sorting_time(stored_data, sort_key)
        
        print("\nTemps d'exécution des algorithmes :")
        for algo, t in times.items():
            print(f"{algo}: {t:.2f} ms")
        
        best_algo = min(times, key=times.get)
        print(f"\nL'algorithme le plus rapide est : {best_algo}")
    else:
        print("Échec de la récupération des données.")

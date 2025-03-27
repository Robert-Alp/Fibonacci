import requests
from collections import deque
import time

class NewsFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"

    def fetch_news(self, q: str, countryCode="fr", page_size=10):
        try:
            params = {
                "countryCode": countryCode,
                "pageSize": page_size,
                "apiKey": self.api_key,
                "q": q
            }
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                articles = [(article["title"], article["url"]) for article in data["articles"]]
                return articles
            else:
                print(f"Erreur HTTP {response.status_code}: Impossible de récupérer les actualités")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion: {e}")
            return []

class NewsQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, article):
        self.queue.append(article)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.popleft()
        print("La file d'attente est vide !")
        return None

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

class NewsStack:
    def __init__(self):
        self.stack = []

    def push(self, article):
        self.stack.append(article)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        print("L'historique est vide !")
        return None

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

def main():
    API_KEY = "7e0496ef5ae0418d88f4b2ade45b712e"
    news_fetcher = NewsFetcher(API_KEY)
    # print(news_fetcher.fetch_news(q="tesla"))
    news_queue = NewsQueue()
    news_stack = NewsStack()
    while True:
        print("\n=== Gestion des Flux d'Actualités ===")
        choice = input("Quel article voulez vous rechercher ? (exemple: telsa): ")
        articles = news_fetcher.fetch_news(q=choice)
        for article in articles:
            news_queue.enqueue(article)
        if len(articles) > 0:
            print(articles)

            break
        print("L'article est vide, recherchez un autre")

    while True:
        print("\n=== Gestion des Flux d'Actualités ===")
        print("1. Lire un article de la file")
        print("2. Afficher le dernier article lu (historique)")
        print("3. Quitter")
        print(f"Articles en attente: {news_queue.size()} | Historique: {news_stack.size()}")

        choice = input("Votre choix (1-3): ")

        if choice == "1":
            article = news_queue.dequeue()
            if article:
                title, url = article
                print(f"\nArticle: {title}")
                print(f"Lien: {url}")
                news_stack.push(article)
                time.sleep(1)  

        elif choice == "2":
            article = news_stack.pop()
            if article:
                title, url = article
                print(f"\nDernier article lu: {title}")
                print(f"Lien: {url}")
                news_stack.push(article)
            time.sleep(1)

        elif choice == "3":
            print("Au revoir !")
            break

        else:
            print("Choix invalide, veuillez entrer 1, 2 ou 3.")
            time.sleep(1)

if __name__ == "__main__":
    main()
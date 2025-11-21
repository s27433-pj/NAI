"""
TMDB Index Builder – NAI 2025
Skrypt pobiera dane o filmach i serialach z TMDB na podstawie tytułów z ratings_tmdb_clean.json
i zapisuje je do tmdb_index.json w celu wzbogacenia systemu rekomendacji o metadane.
"""

import json
import time
import requests

RATINGS_FILE = "ratings_tmdb_clean.json"
OUTPUT_FILE = "tmdb_index.json"

TMDB_API_KEY = ""
TMDB_BASE_URL = "https://api.themoviedb.org/3/search/multi"
LANGUAGE = "pl-PL"


def load_titles():
    """Wczytuje unikalną listę tytułów z pliku ocen użytkowników."""
    with open(RATINGS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    titles = set()
    for user_ratings in data.values():
        titles.update(user_ratings.keys())
    return sorted(titles)


def search_tmdb(title):
    """Wysyła zapytanie do TMDB i zwraca metadane pierwszego najlepszego wyniku."""
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": LANGUAGE,
        "include_adult": False
    }

    response = requests.get(TMDB_BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    results = data.get("results", [])
    if not results:
        return None

    best = results[0]
    return {
        "tmdb_id": best.get("id"),
        "media_type": best.get("media_type"),
        "name": best.get("title") or best.get("name"),
        "original_title": best.get("original_title") or best.get("original_name"),
        "release_date": best.get("release_date") or best.get("first_air_date"),
        "vote_average": best.get("vote_average"),
    }


def main():
    """Buduje indeks TMDB dla wszystkich tytułów i zapisuje go do pliku JSON."""
    titles = load_titles()
    print(f"Znaleziono {len(titles)} unikalnych tytułów.")

    index = {}
    for i, title in enumerate(titles, start=1):
        print(f"[{i}/{len(titles)}] Szukam: {title!r}")
        try:
            info = search_tmdb(title)
            index[title] = info
        except Exception as e:
            print(f"  Błąd dla {title!r}: {e}")
            index[title] = None

        time.sleep(0.25)  # aby nie spamować API

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"Zapisano mapę TMDB do: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

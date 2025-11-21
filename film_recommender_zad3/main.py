"""
NAI – ćwiczenia 08.11.2025
Prosty system rekomendacji filmów i seriali oparty na Pearson correlation oraz filtracji kolaboratywnej user–user.

Instrukcja użycia:
1. Wygeneruj ratings_tmdb_clean.json (normalize_ratings.py).
2. Wygeneruj tmdb_index.json (tmdb_index.py, wymaga TMDB_API_KEY).
3. Uruchom:
       python main.py
4. Wybierz użytkownika — program wypisze 5 rekomendacji i 5 antyrekomendacji.
"""

import json
from compute_scores import pearson_score

RATINGS_FILE = "ratings_tmdb_clean.json"
TMDB_FILE = "tmdb_index.json"


def load_ratings():
    """Wczytuje słownik ocen użytkowników z pliku JSON."""
    with open(RATINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_tmdb_index():
    """Wczytuje słownik metadanych filmów z pliku tmdb_index.json."""
    with open(TMDB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_similarities(data, target_user):
    """Oblicza podobieństwo (Pearson) między użytkownikiem a resztą."""
    sims = {}
    for other in data:
        if other != target_user:
            sims[other] = pearson_score(data, target_user, other)
    return sims


def predict_ratings(data, target_user, min_sim=0.1):
    """Przewiduje oceny filmów, których użytkownik nie widział, używając user-based CF."""
    if target_user not in data:
        raise ValueError(f"Nie ma takiego użytkownika: {target_user}")

    user_ratings = data[target_user]
    sims = compute_similarities(data, target_user)

    totals = {}
    sim_sums = {}

    for other_user, sim in sims.items():
        if sim <= min_sim:
            continue

        for title, rating in data[other_user].items():
            if title in user_ratings:
                continue

            totals.setdefault(title, 0.0)
            sim_sums.setdefault(title, 0.0)

            totals[title] += sim * rating
            sim_sums[title] += sim

    predictions = {}
    for title in totals:
        if sim_sums[title] > 0:
            predictions[title] = totals[title] / sim_sums[title]

    return predictions


def top_n(predictions, n=5):
    """Zwraca N najwyżej ocenionych przewidywań."""
    return sorted(predictions.items(), key=lambda x: x[1], reverse=True)[:n]


def bottom_n(predictions, n=5):
    """Zwraca N najniżej ocenionych przewidywań."""
    return sorted(predictions.items(), key=lambda x: x[1])[:n]


def print_with_tmdb(title, score, tmdb_index):
    """Wypisuje film wraz z informacjami z TMDB (jeśli dostępne)."""
    info = tmdb_index.get(title, {})
    print(f"\nTytuł: {title} (przewidywana ocena: {score:.2f})")

    if info:
        print(f"  TMDB nazwa: {info.get('name')}")
        print(f"  Typ: {info.get('media_type')}")
        print(f"  Premiera: {info.get('release_date')}")
        print(f"  Średnia ocena TMDB: {info.get('vote_average')}")
    else:
        print("  Brak danych TMDB.")


def main():
    """Główna funkcja programu — ładuje dane, wybiera użytkownika i generuje rekomendacje."""
    ratings = load_ratings()
    tmdb_index = load_tmdb_index()

    users = sorted(ratings.keys())
    print("Dostępni użytkownicy:")
    for u in users:
        print(" -", u)

    user = input("\nPodaj nazwę użytkownika dokładnie jak w JSON-ie: ").strip()
    if user not in ratings:
        print("Nie ma takiego użytkownika.")
        return

    predictions = predict_ratings(ratings, user)
    if not predictions:
        print("Brak rekomendacji – za mało danych.")
        return

    best5 = top_n(predictions, 5)
    worst5 = bottom_n(predictions, 5)

    print("\n" + "=" * 60)
    print(f"TOP 5 filmów polecanych dla użytkownika: {user}")
    print("=" * 60)
    for title, score in best5:
        print_with_tmdb(title, score, tmdb_index)

    print("\n" + "=" * 60)
    print(f"TOP 5 filmów, których lepiej NIE polecać użytkownikowi: {user}")
    print("=" * 60)
    for title, score in worst5:
        print_with_tmdb(title, score, tmdb_index)


if __name__ == "__main__":
    main()

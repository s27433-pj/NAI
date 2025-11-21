"""
Normalize Ratings – NAI 2025
Skrypt porządkujący dane filmowe: poprawia literówki tytułów, ujednolica nazwy
i sortuje użytkowników oraz filmy dla spójnego przetwarzania w systemie rekomendacji.
"""

import json
from collections import OrderedDict


INPUT_FILE = "ratings_tmdb.json"
OUTPUT_FILE = "ratings_tmdb_clean.json"


TITLE_MAPPING = {
    "Niebieskoki Samuraj": "Niebieskooki Samuraj",
    "Kapitan Philips": "Kapitan Phillips",
    "Intersellar": "Interstellar",
    "LoTR": "Władca Pierścieni",
    "Auto 2": "Auta 2",
    "forest gump": "Forrest Gump",
    "Fight club": "Fight Club",
    "Fight club ": "Fight Club",
    "Kill bill": "Kill Bill",
    "Kill bill 2": "Kill Bill 2",
    "Pullp fiction": "Pulp Fiction",
    "Leon zawdowiec": "Leon Zawodowiec",
    "Chlopaki nie placza": "Chłopaki nie płaczą",
    "Big. Bang.": "The Big Bang Theory",
    "Dr strange": "Doctor Strange",
    "Star wars": "Star Wars",
    "fullmetal alchemist brotherhood": "Fullmetal Alchemist: Brotherhood",
    "stowarzyszenie umarlych poetow": "Stowarzyszenie umarłych poetów",
    "miedzy pieklem a niebiem": "Między piekłem a niebem",
    "Smarzone zielone pomidory": "Smażone zielone pomidory",
    "Planeta singli": "Planeta Singli",
    "Listi do M.": "Listy do M.",
    "List do M.": "Listy do M.",
    "List do M. 2": "Listy do M. 2",
    "Listy do M. 2": "Listy do M. 2"
}


def normalize_dataset(dataset, mapping):
    """Zamienia błędne tytuły na poprawne według mapowania i usuwa duplikaty."""
    normalized = {}
    for user, ratings in dataset.items():
        new_ratings = {}
        for raw_title, score in ratings.items():
            title = raw_title.strip()
            title = mapping.get(title, title)
            new_ratings[title] = score
        normalized[user] = new_ratings
    return normalized



with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)


normalized = normalize_dataset(data, TITLE_MAPPING)


sorted_data = OrderedDict()
for user in sorted(normalized.keys()):
    movies = normalized[user]
    sorted_movies = OrderedDict(sorted(movies.items(), key=lambda kv: kv[0]))
    sorted_data[user] = sorted_movies


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(sorted_data, f, ensure_ascii=False, indent=2)

print(f"Zapisano poprawiony JSON do: {OUTPUT_FILE}")

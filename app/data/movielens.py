import pandas as pd


def load_ratings(data_path: str) -> pd.DataFrame:
    columns = ["user_id", "item_id", "rating", "timestamp"]
    df = pd.read_csv(data_path, sep="\t", names=columns)
    df.drop(columns="timestamp", inplace=True)
    return df.pivot(index="user_id", columns="item_id", values="rating")


def load_item_names(item_path: str) -> dict[int, str]:
    col_names = ["movie_id", "movie_title"] + [f"f{i}" for i in range(22)]
    items = pd.read_csv(item_path, sep="|", names=col_names, encoding="latin-1")
    return dict(zip(items["movie_id"], items["movie_title"]))


def search_movie(query: str, item_names: dict[int, str]) -> list[tuple[int, str]]:
    q = query.lower()
    results = [(item_id, title) for item_id, title in item_names.items() if q in title.lower()]
    return results[:5]

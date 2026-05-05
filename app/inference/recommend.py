import pandas as pd
from app.model.item_based import predict_rating, predict_for_new_user


def recommend(
    user_id: int,
    matrix: pd.DataFrame,
    sim_matrix: pd.DataFrame,
    item_names: dict[int, str],
    n: int = 10,
    k: int = 10,
) -> list[tuple[str, float]]:
    if user_id not in matrix.index:
        return []

    rated = matrix.loc[user_id].dropna().index
    unrated = [i for i in matrix.columns if i not in rated]

    predictions = [
        (item_names.get(item_id, str(item_id)), predict_rating(user_id, item_id, matrix, sim_matrix, k))
        for item_id in unrated
    ]

    predictions.sort(key=lambda x: x[1], reverse=True)
    return predictions[:n]


def recommend_new(
    user_ratings: dict[int, float],
    matrix: pd.DataFrame,
    sim_matrix: pd.DataFrame,
    item_names: dict[int, str],
    n: int = 10,
    k: int = 10,
) -> list[tuple[str, float]]:
    return predict_for_new_user(user_ratings, matrix, sim_matrix, item_names, n=n, k=k)

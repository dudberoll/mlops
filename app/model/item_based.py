import pandas as pd


def build_similarity_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    # matrix.corr() считает Пирсона по парным наблюдениям — эквивалентно
    # ручному циклу, но векторизовано (секунды вместо минут на ML-100k)
    return matrix.corr(method="pearson")


def predict_rating(
    user_id: int,
    item_id: int,
    matrix: pd.DataFrame,
    sim_matrix: pd.DataFrame,
    k: int = 10,
) -> float:
    if item_id not in matrix.columns or user_id not in matrix.index:
        return 0.0

    user_ratings = matrix.loc[user_id].dropna()
    rated_items = [i for i in user_ratings.index if i != item_id and i in sim_matrix.columns]

    if not rated_items:
        return 0.0

    similarities = sim_matrix.loc[item_id, rated_items]
    top_k_idx = similarities.abs().nlargest(k).index
    top_sims = similarities[top_k_idx]
    top_ratings = user_ratings[top_k_idx]

    mean_i = float(matrix[item_id].mean())
    means_j = matrix[top_k_idx].mean()

    numerator = float((top_sims * (top_ratings - means_j)).sum())
    denominator = float(top_sims.abs().sum())

    return mean_i if denominator == 0.0 else float(mean_i + numerator / denominator)


def predict_for_new_user(
    user_ratings: dict[int, float],
    matrix: pd.DataFrame,
    sim_matrix: pd.DataFrame,
    item_names: dict[int, str],
    n: int = 10,
    k: int = 10,
) -> list[tuple[str, float]]:
    rated_ids = set(user_ratings.keys())
    unrated = [i for i in matrix.columns if i not in rated_ids and i in sim_matrix.columns]
    candidates = [i for i in rated_ids if i in sim_matrix.columns]

    predictions: list[tuple[str, float]] = []

    for item_id in unrated:
        if not candidates:
            continue

        similarities = sim_matrix.loc[item_id, candidates]
        top_k_idx = similarities.abs().nlargest(k).index
        top_sims = similarities[top_k_idx]
        top_ratings = pd.Series({i: user_ratings[i] for i in top_k_idx})

        mean_i = float(matrix[item_id].mean())
        means_j = matrix[list(top_k_idx)].mean()

        numerator = float((top_sims * (top_ratings - means_j)).sum())
        denominator = float(top_sims.abs().sum())

        score = mean_i if denominator == 0.0 else float(mean_i + numerator / denominator)
        predictions.append((item_names.get(item_id, str(item_id)), score))

    predictions.sort(key=lambda x: x[1], reverse=True)
    return predictions[:n]

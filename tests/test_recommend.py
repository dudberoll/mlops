import pandas as pd
from app.inference.recommend import recommend


def test_excludes_already_rated(small_matrix, sim_matrix, item_names):
    rated_titles = {item_names[i] for i in small_matrix.loc[1].dropna().index}
    recs = recommend(1, small_matrix, sim_matrix, item_names, n=10)
    for title, _ in recs:
        assert title not in rated_titles


def test_results_sorted_descending(small_matrix, sim_matrix, item_names):
    recs = recommend(1, small_matrix, sim_matrix, item_names, n=10)
    scores = [s for _, s in recs]
    assert scores == sorted(scores, reverse=True)


def test_cold_start_returns_empty(small_matrix, sim_matrix, item_names):
    assert recommend(999, small_matrix, sim_matrix, item_names) == []


def test_respects_n(small_matrix, sim_matrix, item_names):
    recs = recommend(1, small_matrix, sim_matrix, item_names, n=1)
    assert len(recs) <= 1

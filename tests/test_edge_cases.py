from app.model.item_based import predict_rating
from app.inference.recommend import recommend_new


def test_zero_denominator_no_crash(small_matrix, sim_matrix):
    result = predict_rating(1, 3, small_matrix, sim_matrix, k=10)
    assert isinstance(result, float)


def test_new_user_excludes_rated(small_matrix, sim_matrix, item_names):
    user_ratings = {1: 5.0, 2: 4.0}
    recs = recommend_new(user_ratings, small_matrix, sim_matrix, item_names, n=5)
    for title, _ in recs:
        assert title not in {"Movie1", "Movie2"}


def test_new_user_empty_ratings(small_matrix, sim_matrix, item_names):
    recs = recommend_new({}, small_matrix, sim_matrix, item_names)
    assert recs == []

import pytest
import pandas as pd
from app.model.item_based import build_similarity_matrix

@pytest.fixture
def small_matrix() -> pd.DataFrame:
    data = {
        1: [5.0, 3.0, None, 1.0],
        2: [4.0, None, 4.0, 1.0],
        3: [1.0, 1.0, 1.0, 5.0],
        4: [None, 3.0, None, 2.0],
    }
    return pd.DataFrame(data, index=[1, 2, 3, 4])


@pytest.fixture
def sim_matrix(small_matrix: pd.DataFrame) -> pd.DataFrame:
    return build_similarity_matrix(small_matrix)


@pytest.fixture
def item_names() -> dict[int, str]:
    return {1: "Movie1", 2: "Movie2", 3: "Movie3", 4: "Movie4"}

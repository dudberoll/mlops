import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.data.movielens import load_ratings, load_item_names
from app.model.item_based import build_similarity_matrix
from app.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    data_path = os.getenv("DATA_PATH", "ml-100k/u.data")
    item_path = os.getenv("ITEM_PATH", "ml-100k/u.item")
    app.state.matrix = load_ratings(data_path)
    app.state.item_names = load_item_names(item_path)
    app.state.sim_matrix = build_similarity_matrix(app.state.matrix)
    yield
    app.state.matrix = None
    app.state.sim_matrix = None
    app.state.item_names = None


app = FastAPI(title="Recommender API", lifespan=lifespan)
app.include_router(router)

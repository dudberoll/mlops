from fastapi import APIRouter, Request
from app.api.schemas import RecommendResponse, RecommendedItem
from app.inference.recommend import recommend

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/recommend", response_model=RecommendResponse)
def get_recommendations(request: Request, user_id: int, n: int = 10):
    recs = recommend(
        user_id,
        request.app.state.matrix,
        request.app.state.sim_matrix,
        request.app.state.item_names,
        n=n,
    )
    return RecommendResponse(
        user_id=user_id,
        items=[RecommendedItem(title=t, score=s) for t, s in recs],
    )

from pydantic import BaseModel


class RecommendedItem(BaseModel):
    title: str
    score: float


class RecommendResponse(BaseModel):
    user_id: int
    items: list[RecommendedItem]

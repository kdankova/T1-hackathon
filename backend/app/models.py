from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class SearchRequest(BaseModel):
    query: str
    top_k: int = 3


class SearchResponse(BaseModel):
    draft: str
    alternatives: List[str]
    results_meta: List[Dict[str, Any]]
    internal_token: Optional[str] = None


class FeedbackRequest(BaseModel):
    original_question: str
    original_answer: str
    edited_answer: str
    note: Optional[str] = None


class FeedbackResponse(BaseModel):
    status: str
    internal_token: str


class Taxonomy(BaseModel):
    category: str
    subcategory: str
    subtopic: str = ""


class QAAddRequest(BaseModel):
    question: str
    answer: str
    taxonomy: Taxonomy


class QAAddResponse(BaseModel):
    status: str


class PendingItem(BaseModel):
    internal_token: str
    original_question: str
    old_answer: str
    edited_answer: str
    suggested_by: Optional[str] = None
    created_at: str


class PendingListResponse(BaseModel):
    items: List[PendingItem]


class ResolveRequest(BaseModel):
    internal_token: str
    action: str  # "approve" or "reject"


class ResolveResponse(BaseModel):
    status: str
    reembedded: bool


class Stats(BaseModel):
    total_pending: int
    total_approved: int
    total_rejected: int
    avg_response_time: str
    category_coverage: Optional[Dict] = None
    operator_activity: Optional[Dict] = None


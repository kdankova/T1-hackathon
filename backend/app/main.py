from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime
from typing import List

from app.models import (
    SearchRequest, SearchResponse, 
    FeedbackRequest, FeedbackResponse,
    QAAddRequest, QAAddResponse,
    PendingListResponse, PendingItem,
    ResolveRequest, ResolveResponse,
    Stats
)
from app.database import init_db, get_session, FeedbackItem, QAQueue, generate_token
from app.rag_service import rag_service

app = FastAPI(title="RAG Support API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await init_db()
    print("Database initialized. RAG will initialize on first request.")


@app.get("/")
async def root():
    return {"status": "ok", "message": "RAG Support API is running"}


@app.post("/api/search", response_model=SearchResponse)
async def search_answer(request: SearchRequest):
    try:
        if rag_service.vector_store is None:
            print("Initializing RAG service...")
            await rag_service.initialize()
        result = await rag_service.search(request.query, request.top_k)
        return SearchResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска: {str(e)}")


@app.post("/api/feedback", response_model=FeedbackResponse)
async def send_feedback(
    request: FeedbackRequest,
    session: AsyncSession = Depends(get_session)
):
    try:
        token = generate_token()
        
        feedback = FeedbackItem(
            internal_token=token,
            original_question=request.original_question,
            old_answer=request.old_answer,
            edited_answer=request.edited_answer,
            note=request.note,
            status="pending"
        )
        
        session.add(feedback)
        await session.commit()
        
        return FeedbackResponse(status="received", internal_token=token)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения feedback: {str(e)}")




@app.get("/api/moderation/pending", response_model=PendingListResponse)
async def get_pending_feedback(session: AsyncSession = Depends(get_session)):
    try:
        feedback_result = await session.execute(
            select(FeedbackItem).where(FeedbackItem.status == "pending").order_by(FeedbackItem.created_at)
        )
        feedback_items = feedback_result.scalars().all()
        
        qa_result = await session.execute(
            select(QAQueue).where(QAQueue.status == "pending").order_by(QAQueue.created_at)
        )
        qa_items = qa_result.scalars().all()
        
        items = list(feedback_items) + [
            type('FeedbackItem', (), {
                'id': qa.id,
                'question': qa.question,
                'answer': qa.answer,
                'category': qa.category,
                'subcategory': qa.subcategory,
                'status': qa.status,
                'created_at': qa.created_at,
                'internal_token': f'qa_{qa.id}'
            })() for qa in qa_items
        ]
        
        pending_items = [
            PendingItem(
                internal_token=item.internal_token,
                original_question=item.original_question,
                old_answer=item.old_answer,
                edited_answer=item.edited_answer,
                suggested_by=item.suggested_by,
                created_at=item.created_at.isoformat()
            )
            for item in items
        ]
        
        return PendingListResponse(items=pending_items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения списка: {str(e)}")


@app.post("/api/moderation/resolve", response_model=ResolveResponse)
async def resolve_feedback(
    request: ResolveRequest,
    session: AsyncSession = Depends(get_session)
):
    try:
        result = await session.execute(
            select(FeedbackItem).where(FeedbackItem.internal_token == request.internal_token)
        )
        item = result.scalar_one_or_none()
        
        if not item:
            raise HTTPException(status_code=404, detail="Правка не найдена")
        
        if request.action == "approve":
            item.status = "approved"
            item.resolved_at = datetime.utcnow()
            await session.commit()
            
            await rag_service.rebuild_index_for_item(
                question=item.original_question,
                new_answer=item.edited_answer,
                taxonomy={}
            )
            
            return ResolveResponse(status="applied", reembedded=True)
        
        elif request.action == "reject":
            item.status = "rejected"
            item.resolved_at = datetime.utcnow()
            await session.commit()
            
            return ResolveResponse(status="rejected", reembedded=False)
        
        else:
            raise HTTPException(status_code=400, detail="Неверное действие")
            
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка обработки: {str(e)}")


@app.get("/api/moderation/stats", response_model=Stats)
async def get_moderation_stats(session: AsyncSession = Depends(get_session)):
    try:
        total_pending = await session.scalar(
            select(func.count()).select_from(FeedbackItem).where(FeedbackItem.status == "pending")
        )
        
        total_approved = await session.scalar(
            select(func.count()).select_from(FeedbackItem).where(FeedbackItem.status == "approved")
        )
        
        total_rejected = await session.scalar(
            select(func.count()).select_from(FeedbackItem).where(FeedbackItem.status == "rejected")
        )
        
        return Stats(
            total_pending=total_pending or 0,
            total_approved=total_approved or 0,
            total_rejected=total_rejected or 0,
            avg_response_time="N/A",
            category_coverage=None,
            operator_activity=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения статистики: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


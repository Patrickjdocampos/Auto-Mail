from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import EmailAnalysis
from app.schemas.email import EmailAnalysisRequest, EmailAnalysisResponse
from app.services.llm_service import LLMService

router = APIRouter()


@router.post("/analyze-email", response_model=EmailAnalysisResponse)
def analyze_email(payload: EmailAnalysisRequest, db: Session = Depends(get_db)):
    try:
        service = LLMService()
        result = service.analyze_email(
            subject=payload.subject,
            sender=payload.sender,
            body=payload.body,
        )

        analysis = EmailAnalysis(
            subject=payload.subject,
            sender=payload.sender,
            body=payload.body,
            category=result["category"],
            summary=result["summary"],
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return analysis

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/analyses", response_model=list[EmailAnalysisResponse])
def list_analyses(db: Session = Depends(get_db)):
    return db.query(EmailAnalysis).all()


@router.get("/analyses/{analysis_id}", response_model=EmailAnalysisResponse)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    analysis = db.query(EmailAnalysis).filter(EmailAnalysis.id == analysis_id).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return analysis
from pydantic import BaseModel, Field


class EmailAnalysisRequest(BaseModel):
    subject: str = Field(..., example="Urgent invoice payment reminder")
    sender: str = Field(..., example="billing@company.com")
    body: str = Field(..., example="Your invoice is overdue. Please make payment today.")


class EmailAnalysisResponse(BaseModel):
    id: int
    category: str
    summary: str

    class Config:
        from_attributes = True
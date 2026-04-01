from sqlalchemy import Column, Integer, String, Text

from app.db.database import Base


class EmailAnalysis(Base):
    __tablename__ = "email_analyses"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255), nullable=False)
    sender = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    summary = Column(Text, nullable=False)
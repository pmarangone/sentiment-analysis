from dataclasses import dataclass
from datetime import date
from typing import Dict, Optional
import uuid

@dataclass
class Review:
    customer_id: uuid.UUID
    company_id: uuid.UUID
    review_date: date
    review_data: str
    id: Optional[uuid.UUID] = None
    classification: Optional[str] = None
    classified_at: Optional[date] = None
    sentiment_scores: Optional[Dict[str, float]] = None

@dataclass
class Customer:
    name: str
    id: Optional[uuid.UUID] = None

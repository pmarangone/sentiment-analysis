from sqlalchemy import Column, Date, ForeignKey, String, JSON, Index
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
import uuid

from app.db.schemas import Base


class CompanySchema(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)

    reviews = relationship("ReviewSchema", back_populates="company")

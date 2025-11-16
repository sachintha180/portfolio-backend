from datetime import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime, func


class TimestampedModel(SQLModel):
    created_at: datetime = Field(
        sa_column=Column[datetime](
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )
    updated_at: datetime = Field(
        sa_column=Column[datetime](
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
    )

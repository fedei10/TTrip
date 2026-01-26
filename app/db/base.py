from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from typing import Optional
from datetime import datetime
import uuid


class Base(DeclarativeBase):
    pass

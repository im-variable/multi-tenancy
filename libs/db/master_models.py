from datetime import datetime

from sqlalchemy import DateTime, Float, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    tenant_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    domain: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    isolation_type: Mapped[str] = mapped_column(String(32), nullable=False)
    schema_name: Mapped[str | None] = mapped_column(String(128))
    database_name: Mapped[str | None] = mapped_column(String(128))
    plan: Mapped[str] = mapped_column(String(64), default="standard")
    region: Mapped[str] = mapped_column(String(64), default="ap-south-1")
    status: Mapped[str] = mapped_column(String(32), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Claim(Base):
    __tablename__ = "claims"

    claim_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="created")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class NotificationLog(Base):
    __tablename__ = "notification_logs"

    notification_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    channel: Mapped[str] = mapped_column(String(32), nullable=False)
    recipient: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="queued")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

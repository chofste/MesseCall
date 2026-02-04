from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SqlEnum, ForeignKey, Integer, String
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Role(str, Enum):
    admin = "admin"
    coordinator = "coordinator"
    server = "server"


class AssignmentStatus(str, Enum):
    proposed = "proposed"
    approved = "approved"
    swapped = "swapped"


class SwapStatus(str, Enum):
    open = "open"
    accepted = "accepted"
    declined = "declined"


class NotificationStatus(str, Enum):
    pending = "pending"
    sent = "sent"


class Church(Base):
    __tablename__ = "churches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    timezone: Mapped[str] = mapped_column(String, default="Europe/Berlin")
    public_token: Mapped[str] = mapped_column(String, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="church")
    events = relationship("Event", back_populates="church")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    role: Mapped[Role] = mapped_column(SqlEnum(Role), nullable=False)
    church_id: Mapped[int] = mapped_column(ForeignKey("churches.id"), nullable=False)
    experience_level: Mapped[int] = mapped_column(Integer, default=1)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    church = relationship("Church", back_populates="users")
    preferences = relationship("Preference", back_populates="user", uselist=False)
    assignments = relationship("Assignment", back_populates="user")
    notifications = relationship("Notification", back_populates="user")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    church_id: Mapped[int] = mapped_column(ForeignKey("churches.id"), nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    required_slots: Mapped[int] = mapped_column(Integer, default=1)
    requires_experienced: Mapped[bool] = mapped_column(Boolean, default=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[str] = mapped_column(String, default="")

    church = relationship("Church", back_populates="events")
    assignments = relationship("Assignment", back_populates="event")
    volunteers = relationship("VolunteerInterest", back_populates="event")


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[AssignmentStatus] = mapped_column(
        SqlEnum(AssignmentStatus),
        default=AssignmentStatus.proposed,
    )
    source: Mapped[str] = mapped_column(String, default="algorithm")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    event = relationship("Event", back_populates="assignments")
    user = relationship("User", back_populates="assignments")
    swap_request = relationship("SwapRequest", back_populates="assignment", uselist=False)


class Preference(Base):
    __tablename__ = "preferences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    preferred_weekdays: Mapped[list[str]] = mapped_column(JSON, default=list)
    preferred_time_ranges: Mapped[list[str]] = mapped_column(JSON, default=list)
    preferred_locations: Mapped[list[str]] = mapped_column(JSON, default=list)
    partner_user_ids: Mapped[list[int]] = mapped_column(JSON, default=list)
    favorite_event_types: Mapped[list[str]] = mapped_column(JSON, default=list)

    user = relationship("User", back_populates="preferences")


class Availability(Base):
    __tablename__ = "availabilities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    available: Mapped[bool] = mapped_column(Boolean, default=True)
    note: Mapped[str] = mapped_column(String, default="")


class VolunteerInterest(Base):
    __tablename__ = "volunteer_interests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    note: Mapped[str] = mapped_column(String, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    event = relationship("Event", back_populates="volunteers")


class SwapRequest(Base):
    __tablename__ = "swap_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignments.id"), nullable=False)
    status: Mapped[SwapStatus] = mapped_column(SqlEnum(SwapStatus), default=SwapStatus.open)
    requested_user_ids: Mapped[list[int]] = mapped_column(JSON, default=list)
    replacement_user_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    assignment = relationship("Assignment", back_populates="swap_request")


class BackupPool(Base):
    __tablename__ = "backup_pool"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    preferred_locations: Mapped[list[str]] = mapped_column(JSON, default=list)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class Gamification(Base):
    __tablename__ = "gamification"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    points: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    badges: Mapped[list[str]] = mapped_column(JSON, default=list)
    streak: Mapped[int] = mapped_column(Integer, default=0)


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    message: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[NotificationStatus] = mapped_column(
        SqlEnum(NotificationStatus),
        default=NotificationStatus.pending,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")

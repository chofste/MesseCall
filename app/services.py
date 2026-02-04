from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from . import models


class ScoredCandidate:
    def __init__(self, user_id: int, score: float, reason: str) -> None:
        self.user_id = user_id
        self.score = score
        self.reason = reason


def _load_availability(db: Session, event: models.Event) -> set[int]:
    availability = (
        db.query(models.Availability)
        .filter(
            models.Availability.start_time <= event.start_time,
            models.Availability.end_time >= event.end_time,
            models.Availability.available.is_(True),
        )
        .all()
    )
    return {item.user_id for item in availability}


def _assignment_counts(db: Session, church_id: int) -> dict[int, int]:
    counts: dict[int, int] = defaultdict(int)
    assignments = (
        db.query(models.Assignment)
        .join(models.Event, models.Assignment.event_id == models.Event.id)
        .filter(models.Event.church_id == church_id)
        .all()
    )
    for assignment in assignments:
        counts[assignment.user_id] += 1
    return counts


def suggest_assignments(db: Session, event: models.Event) -> List[ScoredCandidate]:
    available_users = _load_availability(db, event)
    assignment_counts = _assignment_counts(db, event.church_id)
    volunteers = {
        volunteer.user_id
        for volunteer in db.query(models.VolunteerInterest)
        .filter(models.VolunteerInterest.event_id == event.id)
        .all()
    }

    candidates: list[ScoredCandidate] = []
    users = (
        db.query(models.User)
        .filter(
            models.User.church_id == event.church_id,
            models.User.active.is_(True),
            models.User.role == models.Role.server,
        )
        .all()
    )
    for user in users:
        if user.id not in available_users:
            continue
        if event.requires_experienced and user.experience_level < 2:
            continue
        score = float(assignment_counts.get(user.id, 0))
        reasons: list[str] = ["Fairness basierend auf bisherigen Einsätzen"]
        preference = db.query(models.Preference).filter_by(user_id=user.id).first()
        if preference:
            if event.location in preference.preferred_locations:
                score -= 1.0
                reasons.append("Bevorzugter Ort")
            if event.type in preference.favorite_event_types:
                score -= 0.5
                reasons.append("Lieblingsgottesdienst")
            if preference.partner_user_ids:
                if any(partner_id in available_users for partner_id in preference.partner_user_ids):
                    score -= 0.25
                    reasons.append("Wunschpartner verfügbar")
        if user.id in volunteers:
            score -= 1.5
            reasons.append("Freiwillige Zusage")
        candidates.append(ScoredCandidate(user.id, score, "; ".join(reasons)))

    candidates.sort(key=lambda item: item.score)
    return candidates[: event.required_slots]


def create_assignments_from_suggestion(
    db: Session,
    event: models.Event,
    suggestion: List[ScoredCandidate],
) -> list[models.Assignment]:
    assignments: list[models.Assignment] = []
    for item in suggestion:
        assignment = models.Assignment(
            event_id=event.id,
            user_id=item.user_id,
            status=models.AssignmentStatus.proposed,
            source="algorithm",
        )
        db.add(assignment)
        assignments.append(assignment)
    db.commit()
    for assignment in assignments:
        db.refresh(assignment)
    return assignments


def create_swap_request(db: Session, assignment: models.Assignment, requested_user_ids: list[int]) -> models.SwapRequest:
    swap_request = models.SwapRequest(
        assignment_id=assignment.id,
        status=models.SwapStatus.open,
        requested_user_ids=requested_user_ids,
    )
    db.add(swap_request)
    db.commit()
    db.refresh(swap_request)
    return swap_request


def accept_swap_request(
    db: Session,
    swap_request: models.SwapRequest,
    replacement_user_id: int,
) -> models.Assignment:
    assignment = swap_request.assignment
    assignment.user_id = replacement_user_id
    assignment.status = models.AssignmentStatus.swapped
    swap_request.status = models.SwapStatus.accepted
    swap_request.replacement_user_id = replacement_user_id
    db.commit()
    db.refresh(assignment)
    return assignment


def award_points(
    db: Session,
    user_id: int,
    points: int,
    badge: str | None = None,
) -> models.Gamification:
    entry = db.query(models.Gamification).filter_by(user_id=user_id).first()
    if not entry:
        entry = models.Gamification(user_id=user_id, points=0, badges=[], level=1, streak=0)
        db.add(entry)
    entry.points += points
    entry.level = max(1, entry.points // 50 + 1)
    if badge and badge not in entry.badges:
        entry.badges.append(badge)
    entry.streak += 1
    db.commit()
    db.refresh(entry)
    return entry


def create_notification(db: Session, user_id: int, title: str, message: str) -> models.Notification:
    notification = models.Notification(user_id=user_id, title=title, message=message)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def suggest_backup_candidates(db: Session, start_time: datetime, end_time: datetime) -> List[int]:
    pool = (
        db.query(models.BackupPool)
        .filter(
            models.BackupPool.active.is_(True),
            models.BackupPool.start_time <= start_time,
            models.BackupPool.end_time >= end_time,
        )
        .all()
    )
    candidates = [item.user_id for item in pool]
    availability = (
        db.query(models.Availability)
        .filter(
            models.Availability.start_time <= start_time,
            models.Availability.end_time >= end_time,
            models.Availability.available.is_(True),
        )
        .all()
    )
    available_users = {item.user_id for item in availability}
    return [user_id for user_id in candidates if user_id in available_users]


def build_public_events_ics(events: list[models.Event]) -> str:
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//MesseCall//DE"]
    for event in events:
        lines.extend(
            [
                "BEGIN:VEVENT",
                f"UID:event-{event.id}@messecall",
                f"DTSTART:{event.start_time.strftime('%Y%m%dT%H%M%SZ')}",
                f"DTEND:{event.end_time.strftime('%Y%m%dT%H%M%SZ')}",
                f"SUMMARY:{event.type}",
                f"LOCATION:{event.location}",
                f"DESCRIPTION:{event.description}",
                "END:VEVENT",
            ]
        )
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines)

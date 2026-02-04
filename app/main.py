from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session

from . import models, schemas, services
from .database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MesseCall API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/churches", response_model=schemas.ChurchResponse)
def create_church(payload: schemas.ChurchCreate, db: Session = Depends(get_db)):
    church = models.Church(**payload.dict())
    db.add(church)
    db.commit()
    db.refresh(church)
    return church


@app.get("/churches", response_model=list[schemas.ChurchResponse])
def list_churches(db: Session = Depends(get_db)):
    return db.query(models.Church).all()


@app.post("/users", response_model=schemas.UserResponse)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    user = models.User(**payload.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users", response_model=list[schemas.UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.post("/events", response_model=schemas.EventResponse)
def create_event(payload: schemas.EventCreate, db: Session = Depends(get_db)):
    event = models.Event(**payload.dict())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@app.get("/events", response_model=list[schemas.EventResponse])
def list_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()


@app.get("/public/churches/{church_id}/events", response_model=list[schemas.EventResponse])
def list_public_events(church_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Event)
        .filter(models.Event.church_id == church_id, models.Event.is_public.is_(True))
        .all()
    )


@app.get("/public/churches/{church_id}/events.ics")
def list_public_events_ics(church_id: int, db: Session = Depends(get_db)):
    events = (
        db.query(models.Event)
        .filter(models.Event.church_id == church_id, models.Event.is_public.is_(True))
        .all()
    )
    ics = services.build_public_events_ics(events)
    return Response(content=ics, media_type="text/calendar")


@app.post("/volunteer-interests", response_model=schemas.VolunteerInterestResponse)
def create_volunteer_interest(
    payload: schemas.VolunteerInterestCreate, db: Session = Depends(get_db)
):
    volunteer = models.VolunteerInterest(**payload.dict())
    db.add(volunteer)
    db.commit()
    db.refresh(volunteer)
    return volunteer


@app.post("/assignments", response_model=schemas.AssignmentResponse)
def create_assignment(payload: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    assignment = models.Assignment(**payload.dict())
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


@app.get("/assignments", response_model=list[schemas.AssignmentResponse])
def list_assignments(db: Session = Depends(get_db)):
    return db.query(models.Assignment).all()


@app.post("/preferences", response_model=schemas.PreferenceResponse)
def create_preference(payload: schemas.PreferenceCreate, db: Session = Depends(get_db)):
    preference = models.Preference(**payload.dict())
    db.add(preference)
    db.commit()
    db.refresh(preference)
    return preference


@app.post("/availability", response_model=schemas.AvailabilityResponse)
def create_availability(payload: schemas.AvailabilityCreate, db: Session = Depends(get_db)):
    availability = models.Availability(**payload.dict())
    db.add(availability)
    db.commit()
    db.refresh(availability)
    return availability


@app.post("/swap-requests", response_model=schemas.SwapRequestResponse)
def create_swap_request(payload: schemas.SwapRequestCreate, db: Session = Depends(get_db)):
    assignment = (
        db.query(models.Assignment)
        .filter(models.Assignment.id == payload.assignment_id)
        .first()
    )
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    swap_request = services.create_swap_request(db, assignment, payload.requested_user_ids)
    return swap_request


@app.post("/swap-requests/{swap_request_id}/accept", response_model=schemas.AssignmentResponse)
def accept_swap_request(
    swap_request_id: int,
    payload: schemas.SwapRequestAccept,
    db: Session = Depends(get_db),
):
    swap_request = (
        db.query(models.SwapRequest)
        .filter(models.SwapRequest.id == swap_request_id)
        .first()
    )
    if not swap_request:
        raise HTTPException(status_code=404, detail="Swap request not found")
    assignment = services.accept_swap_request(db, swap_request, payload.replacement_user_id)
    services.award_points(db, payload.replacement_user_id, points=10, badge="retter")
    services.create_notification(
        db,
        user_id=payload.replacement_user_id,
        title="Ersatzdienst bestätigt",
        message="Danke, dass du den Ersatzdienst übernommen hast.",
    )
    return assignment


@app.post("/backup-pool", response_model=schemas.BackupPoolResponse)
def create_backup_pool(payload: schemas.BackupPoolCreate, db: Session = Depends(get_db)):
    pool = models.BackupPool(**payload.dict())
    db.add(pool)
    db.commit()
    db.refresh(pool)
    return pool


@app.get("/backup-pool/suggestions")
def backup_suggestions(start_time: str, end_time: str, db: Session = Depends(get_db)):
    start_dt = datetime.fromisoformat(start_time)
    end_dt = datetime.fromisoformat(end_time)
    candidates = services.suggest_backup_candidates(db, start_dt, end_dt)
    return {"candidates": candidates}


@app.post("/gamification", response_model=schemas.GamificationResponse)
def create_gamification(payload: schemas.GamificationCreate, db: Session = Depends(get_db)):
    entry = models.Gamification(**payload.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@app.get("/gamification/{user_id}", response_model=schemas.GamificationResponse)
def get_gamification(user_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.Gamification).filter(models.Gamification.user_id == user_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Gamification not found")
    return entry


@app.get("/notifications/{user_id}", response_model=list[schemas.NotificationResponse])
def list_notifications(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Notification).filter(models.Notification.user_id == user_id).all()


@app.post("/events/{event_id}/suggestions", response_model=schemas.PlanSuggestion)
def suggest_plan(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    suggestions = services.suggest_assignments(db, event)
    return schemas.PlanSuggestion(
        event_id=event_id,
        items=[
            schemas.PlanSuggestionItem(
                user_id=item.user_id,
                score=item.score,
                reason=item.reason,
            )
            for item in suggestions
        ],
    )


@app.post("/events/{event_id}/proposals", response_model=list[schemas.AssignmentResponse])
def propose_plan(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    suggestions = services.suggest_assignments(db, event)
    assignments = services.create_assignments_from_suggestion(db, event, suggestions)
    return assignments


@app.post("/assignments/{assignment_id}/approve")
def approve_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = (
        db.query(models.Assignment)
        .filter(models.Assignment.id == assignment_id)
        .first()
    )
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    assignment.status = models.AssignmentStatus.approved
    assignment.approved_at = datetime.utcnow()
    db.commit()
    services.award_points(db, assignment.user_id, points=5, badge="zuverlaessig")
    services.create_notification(
        db,
        user_id=assignment.user_id,
        title="Einsatz bestätigt",
        message="Dein Einsatz wurde bestätigt. Vielen Dank!",
    )
    return {"assignment_id": assignment.id, "status": assignment.status}

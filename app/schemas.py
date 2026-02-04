from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class ChurchBase(BaseModel):
    name: str
    address: str
    timezone: str = "Europe/Berlin"


class ChurchCreate(ChurchBase):
    pass


class ChurchResponse(ChurchBase):
    id: int
    public_token: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str
    church_id: int
    experience_level: int = 1
    active: bool = True


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class EventBase(BaseModel):
    church_id: int
    type: str
    start_time: datetime
    end_time: datetime
    location: str
    required_slots: int = 1
    requires_experienced: bool = False
    is_public: bool = False
    description: str = ""


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: int

    class Config:
        from_attributes = True


class AssignmentBase(BaseModel):
    event_id: int
    user_id: int
    status: str = "proposed"
    source: str = "algorithm"


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentResponse(AssignmentBase):
    id: int
    created_at: datetime
    approved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PreferenceBase(BaseModel):
    user_id: int
    preferred_weekdays: List[str] = Field(default_factory=list)
    preferred_time_ranges: List[str] = Field(default_factory=list)
    preferred_locations: List[str] = Field(default_factory=list)
    partner_user_ids: List[int] = Field(default_factory=list)
    favorite_event_types: List[str] = Field(default_factory=list)


class PreferenceCreate(PreferenceBase):
    pass


class PreferenceResponse(PreferenceBase):
    id: int

    class Config:
        from_attributes = True


class AvailabilityBase(BaseModel):
    user_id: int
    start_time: datetime
    end_time: datetime
    available: bool = True
    note: str = ""


class AvailabilityCreate(AvailabilityBase):
    pass


class AvailabilityResponse(AvailabilityBase):
    id: int

    class Config:
        from_attributes = True


class VolunteerInterestBase(BaseModel):
    event_id: int
    user_id: int
    note: str = ""


class VolunteerInterestCreate(VolunteerInterestBase):
    pass


class VolunteerInterestResponse(VolunteerInterestBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SwapRequestBase(BaseModel):
    assignment_id: int
    status: str = "open"
    requested_user_ids: List[int] = Field(default_factory=list)


class SwapRequestCreate(SwapRequestBase):
    pass


class SwapRequestResponse(SwapRequestBase):
    id: int
    replacement_user_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SwapRequestAccept(BaseModel):
    replacement_user_id: int


class BackupPoolBase(BaseModel):
    user_id: int
    start_time: datetime
    end_time: datetime
    preferred_locations: List[str] = Field(default_factory=list)
    active: bool = True


class BackupPoolCreate(BackupPoolBase):
    pass


class BackupPoolResponse(BackupPoolBase):
    id: int

    class Config:
        from_attributes = True


class GamificationBase(BaseModel):
    user_id: int
    points: int = 0
    level: int = 1
    badges: List[str] = Field(default_factory=list)
    streak: int = 0


class GamificationCreate(GamificationBase):
    pass


class GamificationResponse(GamificationBase):
    id: int

    class Config:
        from_attributes = True


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class PlanSuggestionItem(BaseModel):
    user_id: int
    score: float
    reason: str


class PlanSuggestion(BaseModel):
    event_id: int
    items: List[PlanSuggestionItem]

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Church(Base):
    __tablename__ = "churches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    church_id = Column(Integer, ForeignKey("churches.id"), nullable=False)


class UserCreate(BaseModel):
    name: str
    email: str
    church_id: int


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    church_id: int

    class Config:
        orm_mode = True


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.post("/users", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    church = db.query(Church).filter(Church.id == payload.church_id).first()
    if church is None:
        raise HTTPException(status_code=404, detail="Church not found")

    user = User(name=payload.name, email=payload.email, church_id=payload.church_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

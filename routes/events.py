from typing import List
from fastapi import APIRouter, HTTPException, status, Depends, Request
from database.connection import get_session
from models.events import Event, EventUpdate
from sqlmodel import select

event_router = APIRouter(tags=["Events"])

events = []


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
    """Retrieve all events"""
    statement = select(Event)
    events = session.exec(statement).all()
    return events


@event_router.get("/{event_id}", response_model=Event)
async def retrieve_event(event_id: int, session=Depends(get_session)) -> Event:
    """Filter event by ID"""
    event = session.get(Event, event_id)
    if event:
        return event
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event with supplied ID does not exist")


@event_router.post("/new")
async def create_event(new_event: Event, session=Depends(get_session)) -> dict:
    """Create new event"""
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return {"message": "Event created successfully"}


@event_router.delete("/delete/{event_id}")
async def delete_event(event_id: int, session=Depends(get_session)) -> dict:
    """Remove event by ID"""
    event = session.get(Event, event_id)
    if event:
        session.delete(event)
        session.commit()
        return {"message": "Event deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event with supplied ID does not exist")


@event_router.put("/edit/{event_id}", response_model=Event)
async def update_event(event_id: int, new_data: EventUpdate, session=Depends(get_session)) -> Event:
    """Update event by ID"""
    event = session.get(Event, event_id)
    if event:
        event_data = new_data.dict(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)
        session.add(event)
        session.commit()
        session.refresh(event)
        return event
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event with supplied ID does not exist")

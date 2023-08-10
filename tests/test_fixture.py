import pytest
from models.events import EventUpdate


# Fixture is defined
@pytest.fixture
def event() -> EventUpdate:
    return EventUpdate(
        title="FastAPI Book Launch",
        image="https://packt.com/fastapi.png",
        description="We will be discussing the contents of the FastAPI book in this event.Ensure to come with your "
                    "own copy to win gifts!",
        tags=["python", "fastapi", "book", "launch"],
        location="Google Meet"
    )


def test_event_title(event: EventUpdate) -> None:
    assert event.title == "FastAPI Book Launch"


def test_event_location(event: EventUpdate) -> None:
    assert event.location == "Google Meet"

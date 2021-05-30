from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# TODO: add a mixin for created_at, last_updated_at, and id


# TODO: How do I implement "get all reminders sent to user x" efficiently?
#   Right now have to loop through user's events
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)  # TODO: add index
    phone = Column(String, nullable=False)
    email_verified = Column(Boolean)
    phone_verified = Column(Boolean)
    refresh_token = Column(String)
    last_sync_at = Column(DateTime)

    channels = relationship("Channel")
    events = relationship("Event", back_populates="user")
    # TODO: add reminders (?)

    def __repr__(self):
        return f"<User id={self.id} first_name={self.first_name} email={self.email}>"


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Channel id={self.id} name={self.name}>"


# TODO: add m2m relationship between users and channels


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    calendar_event_id = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="events")
    reminders = relationship("Reminder", back_populates="event")

    def __repr__(self):
        return f"<Event id={self.id} name={self.name}>"


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True)
    event_id = Column(ForeignKey("events.id"), nullable=False)
    channel_id = Column(ForeignKey("channels.id"), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(Enum("in_process", "failed", "sent", name="reminder_statuses"))

    event = relationship("Event", back_populates="reminders")
    channel = relationship("Channel")

    def __repr__(self):
        return f"<Reminder id={self.id}>"


# TODO: Rethink design
#   Subject of log can be any of the other models, not just reminders
#   Example: log by bg process that syncs users' calendar events every 10 mins
class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)
    reminder_id = Column(ForeignKey("reminders.id"))
    details = Column(Text)  # TODO: should be JSONB

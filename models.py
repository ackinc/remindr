from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import declarative_base, declarative_mixin, relationship


Base = declarative_base()


@declarative_mixin
class TimestampsMixin:
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    last_updated_at = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )


users_channels_table = Table(
    "users_channels",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("channel_id", ForeignKey("channels.id")),
)


class User(TimestampsMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, unique=True)
    email_verified = Column(Boolean)
    phone_verified = Column(Boolean)
    refresh_token = Column(String)
    last_sync_at = Column(DateTime)

    channels = relationship("Channel", secondary=users_channels_table)
    events = relationship("Event", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} first_name={self.first_name} email={self.email}>"


class Channel(TimestampsMixin, Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Channel id={self.id} name={self.name}>"


class Event(TimestampsMixin, Base):
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


class Reminder(TimestampsMixin, Base):
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
class Log(TimestampsMixin, Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)
    reminder_id = Column(ForeignKey("reminders.id"))
    data = Column(Text)  # TODO: should be JSONB

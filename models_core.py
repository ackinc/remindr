from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
)


metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("email", String, nullable=False),
    Column("phone", String),
    Column("email_verified", Boolean),
    Column("phone_verified", Boolean),
    Column("refresh_token", String),
    Column("last_sync_at", DateTime),
)

channels_table = Table(
    "channels",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
)

users_channels_table = Table(
    "users_channels",
    metadata,
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("channel_id", ForeignKey("channels.id"), nullable=False),
)

events_table = Table(
    "events",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("calendar_event_id", String, nullable=False),
    Column("start_time", DateTime, nullable=False),
)

reminders_table = Table(
    "reminders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("event_id", ForeignKey("events.id"), nullable=False),
    Column("channel_id", ForeignKey("channels.id"), nullable=False),
    Column("content", Text, nullable=False),
    Column(
        "status", Enum("in_process", "failed", "sent", name="statuses"), nullable=False
    ),
)


# TODO: think about design ("subject" of log can be any of the other models, not just reminders)
logs_table = Table(
    "logs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("source", String, nullable=False),
    Column("reminder_id", ForeignKey("reminders.id")),
    Column("details", String),  # should be JSONB
)

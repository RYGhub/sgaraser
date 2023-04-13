import uuid
import os

import sqlalchemy.orm
import requests
from sqlalchemy import Column, String, LargeBinary, ForeignKey, JSON, DateTime, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

__all__ = (
    "Base",
    "User",
    "Server",
)

Base = sqlalchemy.orm.declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(LargeBinary, nullable=True)
    blocked = Column(Boolean, default=False)

    admin_of = relationship("Server", back_populates="admin")
    times = relationship("Time", back_populates="user")


class Campaign(Base):
    __tablename__ = "campaign"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    over = Column(Boolean, default=False, nullable=True)

    races = relationship("Race", back_populates="campaign")


class Race(Base):
    __tablename__ = "race"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="races")
    times = relationship("Time", back_populates="race")


class Time(Base):
    __tablename__ = "time"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    value = Column(Float, nullable=False)

    race_id = Column(UUID(as_uuid=True), ForeignKey("race.id"))
    race = relationship("Race", back_populates="times")
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="times")


class Server(Base):
    __tablename__ = "server"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    motd = Column(String)
    logo_uri = Column(String)
    custom_colors = Column(JSON)

    admin_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    admin = relationship("User", back_populates="admin_of")

# for global db models
# SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database.
# « Représente exactement comment est structuré la donnée dans la DB. »
# Pour les projets simples --> tous les modèles dans le même fichier.

from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    picture: Mapped[Optional[str]] = mapped_column(String(2048))

    users: Mapped[List["User"]] = relationship(back_populates="city")
    zones: Mapped[List["Zone"]] = relationship(back_populates="city")
    stops: Mapped[List["Stop"]] = relationship(back_populates="city")

class Zone(Base):
    __tablename__ = "zone"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(150))
    picture: Mapped[Optional[str]] = mapped_column(String(2048))

    id_city = mapped_column(ForeignKey("city.id"))

    city: Mapped[City] = relationship(back_populates="zones")
    users: Mapped[List["User"]] = relationship(back_populates="zone")

class Stop(Base):
    __tablename__ = "stop"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(150), nullable=False)
    picture: Mapped[Optional[str]] = mapped_column(String(2048))
    mac_beacon: Mapped[Optional[str]] = mapped_column(String(17), unique=True)

    id_city = mapped_column(ForeignKey("city.id"))

    city: Mapped[City] = relationship(back_populates="stops")

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    name: Mapped[str] = mapped_column(String(50))
    verified: Mapped[bool] = mapped_column(default=False)
    vehicle_model: Mapped[Optional[str]] = mapped_column(String(50))
    vehicle_color: Mapped[Optional[str]] = mapped_column(String(20))
    vehicle_registration: Mapped[Optional[str]] = mapped_column(String(15), unique=True)
    mac_beacon: Mapped[Optional[str]] = mapped_column(String(17), unique=True)
    ticket_balance: Mapped[int] = mapped_column(default=0)

    id_city = mapped_column(ForeignKey("city.id"), nullable=True)
    id_zone = mapped_column(ForeignKey("zone.id"), nullable=True)

    city: Mapped[City] = relationship(back_populates="users")
    zone: Mapped[Zone] = relationship(back_populates="users")

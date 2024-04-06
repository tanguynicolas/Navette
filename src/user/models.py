# for db models
# SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database.
# « Représente exactement comment est structuré la donnée dans la DB. »

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    verified = Column(Boolean, default=False)
    vehicle_model = Column(String)
    vehicle_color = Column(String)
    vehicle_registration =  Column(String, unique=True)
    mac_beacon = Column(String, unique=True)
    id_city = Column(Integer, ForeignKey("city.id"))
    #id_zone = Column(Integer, ForeignKey("zone.id"))

    city = relationship("City", back_populates="users")
    #zones = relationship("Zone", back_populates="users")

class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    users = relationship("User", back_populates="city")

#class Zone(Base):
#    __tablename__ = "zone"
#
#    id = Column(Integer, primary_key=True)
#    name = Column(String)
#    picture = Column(String)
#    description = Column(String)
#
#    users = relationship("User", back_populates="zones")

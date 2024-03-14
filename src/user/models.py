# for db models

from .schemas import VehicleColor, User

users = [
    User(id=1, email="tanguy@nicolas.fr", name="Tanguy", verified=False, vehicle_model=None, vehicle_color=VehicleColor.BLUE, vehicle_registration=None, mac_beacon=None)
]

"""Drivers for the simulation"""

from typing import Optional
from location import Location, manhattan_distance
from rider import Rider


class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    id: A unique identifier for the driver.
    location: The current location of the driver.
    speed: The speed of the car.
    is_idle: True if the driver is idle and False otherwise.
    destination: Location of the desired destination of the driver's route.
    """

    id: str
    location: Location
    speed: int
    is_idle: bool
    destination: Optional[Location]

    def __init__(self, identifier: str, location: Location, speed: int) -> None:
        """Initialize a Driver.

        """
        self.id = identifier
        self.location = location
        self.speed = speed
        self.is_idle = True
        self.destination = None

    def __str__(self) -> str:
        """Return a string representation.

        """
        return (f"Driver(id={self.id}, location={self.location}, "
                f"speed={self.speed}, "
                f"is_idle={self.is_idle}, destination={self.destination})")

    def __eq__(self, other: object) -> bool:
        """Return True if self equals other, and false otherwise.

        """
        if isinstance(other, Driver) and other.id == self.id:
            return True
        return False

    def get_travel_time(self, destination: Location) -> int:
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        """
        distance = manhattan_distance(self.location, destination)
        return round(distance / self.speed)

    def start_drive(self, location: Location) -> int:
        """Start driving to the location.
        Return the time that the drive will take.

        """
        self.destination = location
        self.is_idle = False
        return self.get_travel_time(location)

    def end_drive(self) -> None:
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        """
        self.location = self.destination
        self.destination = None
        self.is_idle = True

    def start_ride(self, rider: Rider) -> int:
        """Start a ride and return the time the ride will take.

        """
        # if rider.patience < self.get_travel_time(rider.dest):
        #     self.destination = None
        #     self.is_idle = True
        #     return 0
        self.destination = rider.dest
        self.location = rider.origin
        self.is_idle = False
        # self.rider = rider
        return self.get_travel_time(self.destination)

    def end_ride(self) -> None:
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        """
        self.location = self.destination
        self.destination = None
        self.is_idle = True
        # self.rider.origin = self.destination
        # self.rider.dest = None
        # self.rider = None


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(
        config={'extra-imports': ['location', 'rider']})

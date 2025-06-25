"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
WAITING: A constant used for the waiting rider status.
CANCELLED: A constant used for the cancelled rider status.
SATISFIED: A constant used for the satisfied rider status
"""

from location import Location

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:

    """A rider for a ride-sharing service.

    === Attributes ===
    id: str - the id of the rider
    wait: int - the time queue of how long the rider will wait
    origin: Location - the location of where the rider is
    dest: Location - the location of the desired destination
    status: str - Used to represent how the rider is waiting for the driver,
    cancelling or being satisfied with the ride.
    """
    id: str
    patience: int
    origin: Location
    dest: Location
    status: str

    def __init__(self, identifier: str, patience: int, origin: Location,
                 destination: Location) -> None:
        """Initialize a Rider.

        """
        self.id = identifier
        self.patience = patience
        self.origin = origin
        self.dest = destination
        self.status = WAITING

    def __str__(self) -> str:
        """The string representation of a Rider."""
        return (f"Rider(id={self.id}, patience={self.patience}, "
                f"origin={self.origin}, "
                f"dest={self.dest}, status={self.status}")

    def __eq__(self, other: object) -> bool:
        """
        Return True if this Rider equals the other Rider,
        and false otherwise.
        """
        if isinstance(other, Rider) and self.id == other.id:
            return True
        return False


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['location']})

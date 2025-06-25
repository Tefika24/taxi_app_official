"""Locations for the simulation"""

from __future__ import annotations


class Location:
    """A two-dimensional location.

    === Attributes ===
    row: int - the first coordinate point
    col: int - the second coordinate point
    """
    row: int
    col: int

    def __init__(self, row: int, column: int) -> None:
        """Initialize a location.

        """
        self.row = row
        self.col = column

    def __str__(self) -> str:
        """Return a string representation.

        """
        return f'({self.row}, {self.col})'

    def __eq__(self, other: Location) -> bool:
        """Return True if self equals other, and false otherwise.

        """
        if other.row == self.row and other.col == self.col:
            return True
        return False


def manhattan_distance(origin: Location, destination: Location) -> int:
    """Return the Manhattan distance between the origin and the destination.

    |x1 - x2| + |y1 - y2|
    """
    return abs(origin.row - destination.row) + abs(origin.col - destination.col)


def deserialize_location(location_str: str) -> Location:
    """Deserialize a location.

    location_str: A location in the format 'row,col'
    """
    stripped = location_str.split(',')
    row = int(stripped[0])
    col = int(stripped[1])
    return Location(row, col)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all()
    
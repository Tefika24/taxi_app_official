"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from __future__ import annotations
from typing import List

from rider import Rider, WAITING, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import deserialize_location
from monitor import Monitor, RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF


class Event:
    """An event.

    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    timestamp: A timestamp for this event.
    """

    timestamp: int

    def __init__(self, timestamp: int) -> None:
        """Initialize an Event with a given timestamp.

        Precondition: timestamp must be a non-negative integer.

        # >>> Event(7).timestamp
        # 7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other: Event) -> bool:
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other: Event) -> bool:
        """Return True iff this Event is not equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other: Event) -> bool:
        """Return True iff this Event is less than <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other: Event) -> bool:
        """Return True iff this Event is less than or equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other: Event) -> bool:
        """Return True iff this Event is greater than <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other

    def __ge__(self, other: Event) -> bool:
        """Return True iff this Event is greater than or equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.

    === Attributes ===
    rider: The rider.
    """

    rider: Rider

    def __init__(self, timestamp: int, rider: Rider) -> None:
        """Initialize a RiderRequest event.

        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        """
        monitor.notify(self.timestamp, RIDER, REQUEST,
                       self.rider.id, self.rider.origin)

        events = []
        driver = dispatcher.request_driver(self.rider)
        if driver is not None:
            travel_time = driver.start_drive(self.rider.origin)
            events.append(Pickup(self.timestamp + travel_time,
                                 self.rider, driver))
        events.append(Cancellation(self.timestamp + self.rider.patience,
                                   self.rider))
        return events

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        r = self.rider.id
        return f"{self.timestamp} -- {r}: Request a driver"


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    driver: The driver.
    """

    driver: Driver

    def __init__(self, timestamp: int, driver: Driver) -> None:
        """Initialize a DriverRequest event.

        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.

        If a rider is available, return a Pickup event.

        """
        # Notify the monitor about the request.
        x = self.driver.id
        y = self.driver.location
        monitor.notify(self.timestamp, DRIVER, REQUEST, x, y)
        # Request a rider from the dispatcher.
        events = []
        rider = dispatcher.request_rider(self.driver)
        if rider is not None:
            # self.driver.destination = rider.origin
            # self.driver.rider = rider
            time = self.driver.start_drive(rider.origin)
            # self.driver.destination = rider.origin
            # self.timestamp += driving_time
            d = self.driver
            r = rider
            events.append(Pickup(self.timestamp + time, r, d))
        # If there is one available, the driver starts driving towards the
        # rider, and the method returns a Pickup event for when the driver
        # arrives at the riders location.
        return events

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        d = self.driver.id
        return f"{self.timestamp} -- {d}: Request a rider"


class Cancellation(Event):
    """
    Cancels the rider's request on the up incoming ride
    and registered to the monitor.

    === Attributes ===
    rider: The rider.
    """
    rider: Rider

    def __init__(self, timestamp: int, rider: Rider) -> None:
        """
        Initialize a Cancellation Event
        """
        Event.__init__(self, timestamp)
        self.rider = rider

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """
        Sets the rider to a cancelled status and updates the monitor.
        Returning an empty Event.
        """
        if self.rider.status == WAITING:
            self.rider.status = CANCELLED
            # recently took out self.time + self.rider.patience
            # self.timestamp += self.rider.patience
            i = self.rider.id
            o = self.rider.origin
            monitor.notify(self.timestamp, RIDER, CANCEL, i, o)
            dispatcher.cancel_ride(self.rider)
            # print(len(dispatcher._drivers))
        return []

    def __str__(self) -> str:
        """Return a string representation of the Cancellation Event.

        """
        r = self.rider.id
        return f"{self.timestamp} -- {r}: Rider cancelled"


class Pickup(Event):
    """
    Picks up the rider into the car (of the assigned driver)
    and registers this to the monitor.

    === Attributes ===
    driver: The driver.
    rider: The rider.
    """
    rider: Rider
    driver: Driver

    def __init__(self, timestamp: int, rider: Rider, driver: Driver) -> None:
        """
        Initialize a PickUp Event
        """
        Event.__init__(self, timestamp)
        self.rider = rider
        self.driver = driver

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """
        Set the driver's location and destination to the rider and no longer
        have the rider waiting, notify the monitor about the driver and the
        rider. If the rider cancelled, return a Requested Driver from the
        dispatcher.
        """
        if self.rider.status == WAITING:
            self.driver.end_drive()
            self.rider.status = SATISFIED
            di = self.driver.id
            dl = self.driver.location
            ri = self.rider.id
            ro = self.rider.origin
            monitor.notify(self.timestamp, DRIVER, PICKUP, di, dl)
            monitor.notify(self.timestamp, RIDER, PICKUP, ri, ro)
            travel = self.driver.start_ride(self.rider)
            # self.timestamp += travel
            return [Dropoff(self.timestamp + travel, self.rider, self.driver)]
        elif self.rider.status == CANCELLED:
            self.driver.end_drive()
            return [DriverRequest(self.timestamp, self.driver)]
        return []

    def __str__(self) -> str:
        """Return a string representation of the PickUp event.

        """
        d, r = self.driver.id, self.rider.id
        return f"{self.timestamp} -- {d}: Pick Up rider {r}"


class Dropoff(Event):
    """
    Drops off the rider from the car (of the assigned driver)
    and registers this to the monitor

    === Attributes ===
    driver: The driver.
    rider: The rider.
    """
    rider: Rider
    driver: Driver

    def __init__(self, timestamp: int, rider: Rider, driver: Driver) -> None:
        """
        Initialize a Drop off event
        """
        Event.__init__(self, timestamp)
        self.rider = rider
        self.driver = driver

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """
        Set the location to the rider's destination and make the driver
        wait for a dispatched call of an awaiting rider.
        Returning a Rider.
        """
        # self.driver.location = self.rider.dest
        # self.rider.origin = self.rider.dest
        # self.driver.destination = None
        # self.driver.is_idle = True
        # self.rider.status = SATISFIED
        # self.driver.rider = None
        # drive_time = self.driver.get_travel_time(self.rider.dest)
        self.driver.end_ride()
        ri = self.rider.id
        ro = self.rider.origin
        di = self.driver.id
        dl = self.driver.location
        monitor.notify(self.timestamp, RIDER, DROPOFF, ri, ro)
        monitor.notify(self.timestamp, DRIVER, DROPOFF, di, dl)
        dispatcher.cancel_ride(self.rider)
        # self.driver.end_ride()
        return [DriverRequest(self.timestamp, self.driver)]

    def __str__(self) -> str:
        """Return a string representation of the DropOff Event.

        """
        d = self.driver.id
        r = self.rider.id
        return f"{self.timestamp} -- {d}: Drop off rider {r}"


def create_event_list(filename: str) -> List[Event]:
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    filename: The name of a file that contains the list of events.
    """
    events = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                # Skip lines that are blank or start with #.
                # next(file)
                continue

            # Create a list of words in the line, e.g.
            # ['10', 'RiderRequest', 'Cerise', '4,2', '1,5', '15'].
            # Note that these are strings, and you'll need to convert some
            # of them to a different type.
            tokens = line.split()
            timestamp = int(tokens[0])
            event_type = str(tokens[1])
            loc = deserialize_location(tokens[3])
            # HINT: Use Location.deserialize to convert the location string to
            # a location.
            event = None
            if event_type == "DriverRequest":
                driver = Driver(tokens[2], loc, int(tokens[4]))
                event = DriverRequest(timestamp, driver)
                # Create a DriverRequest event.
                print(f"Created DriverRequest event at"
                      f"{timestamp} for driver {tokens[2]}")

            elif event_type == "RiderRequest":
                loc1 = deserialize_location(tokens[4])
                rider = Rider(tokens[2], int(tokens[5]), loc, loc1)
                event = RiderRequest(timestamp, rider)
                # Create a RiderRequest event.
                # print(f"Created RiderRequest event at"
                #       f"{timestamp} for rider {tokens[2]}")
            if event is not None:
                events.append(event)
                print(f"Parsed event: {event}")
    return events


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(
        config={
            'allowed-io': ['create_event_list'],
            'extra-imports': ['rider', 'dispatcher', 'driver',
                              'location', 'monitor']})

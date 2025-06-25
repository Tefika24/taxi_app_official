"""Dispatcher for the simulation"""

from typing import Optional
from driver import Driver
from rider import Rider


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.
    """
    _waiting_rider: list[Optional[Rider]]  # Queue
    _drivers: list[Optional[Driver]]

    def __init__(self) -> None:
        """Initialize a Dispatcher.

        """
        self._drivers = []
        self._waiting_rider = []

    def __str__(self) -> str:
        """Return a string representation.

        """
        return (f"Dispatcher with {len(self._waiting_rider)} riders waiting "
                f"and {len(self._drivers)} available drivers")

    def request_driver(self, rider: Rider) -> Optional[Driver]:
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        """
        # print(f"Request driver for rider: {rider.id}")
        # Maybe check if driver's travel time be enough for rider's patience.
        if self._drivers == []:
            self._waiting_rider.append(rider)
            # print(f"no drivers yet")
            return None
        temp = None
        for driver in self._drivers:
            time = driver.get_travel_time(rider.origin)

            if driver.is_idle:
                if temp is None:
                    temp = driver
                best_time = temp.get_travel_time(rider.origin)
                if time < best_time:
                    temp = driver
        if temp is None:
            self._waiting_rider.append(rider)
            # print(f"No driver that is quick enough for your patience")
            return None
        # index = self._drivers.index(temp)
        # self._drivers[index].start_drive(rider.origin)
        # temp.start_drive(rider.origin)
        # temp.rider = rider

        # print("Driver", temp.id, "assigned to rider", rider.id)
        # print(len(self._waiting_rider))
        # print(len(self._drivers))
        temp.is_idle = False
        temp.destination = rider.origin
        return temp

    def request_rider(self, driver: Driver) -> Optional[Rider]:
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        """
        rider = None
        if len(self._waiting_rider) > 0:
            rider = self._waiting_rider[0]
            # driver.destination = rider.origin
            # driver.is_idle = False
            self._waiting_rider.remove(rider)
            driver.is_idle = False
            driver.destination = rider.origin
        truth = True
        for ubers in self._drivers:
            if driver.id == ubers.id:
                truth = False
                # print(driver.id)
        if truth:
            self._drivers.append(driver)
        # index = self._drivers.index(driver)
        # if rider:
        #     self._drivers[index].start_drive(rider.origin)
            # print("Rider", rider.id, "assigned to driver", driver.id)
        # print(len(self._waiting_rider))
        # print(len(self._drivers))
        return rider

    def cancel_ride(self, rider: Rider) -> None:
        """Cancel the ride for rider.

        """
        for passenger in self._waiting_rider:
            if rider.id == passenger.id:
                self._waiting_rider.remove(passenger)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['typing', 'driver', 'rider']})

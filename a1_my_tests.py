from driver import Driver
from rider import Rider
from dispatcher import Dispatcher
from location import Location
import pytest


def test_dispatcher():
    driver = Driver('GEO', Location(3, 5), 3)
    rider = Rider('SPA', 10, Location(7, 7), Location(20, 2))
    driver1 = Driver('GEO1', Location(3, 10), 2)
    rider1 = Rider('SPA1', 5, Location(5, 7), Location(2, 2))
    dispatcher = Dispatcher()
    dispatcher.request_rider(driver)
    dispatcher.request_driver(rider)
    assert not dispatcher._drivers[0].is_idle
    assert len(dispatcher._waiting_rider) == 0
    dispatcher.request_driver(rider1)
    dispatcher.request_rider(driver1)
    assert not dispatcher._drivers[0].is_idle
    assert len(dispatcher._waiting_rider) == 0
    rider5 = Rider('SPA1', 2, Location(5, 7), Location(2, 2))
    dispatcher.request_driver(rider5)
    assert len(dispatcher._waiting_rider) == 1
    assert rider5 in dispatcher._waiting_rider
    dispatcher.cancel_ride(rider5)
    assert len(dispatcher._waiting_rider) == 0
    assert rider5 not in dispatcher._waiting_rider

if __name__ == '__main__':
    pytest.main(['a1_my_tests.py'])


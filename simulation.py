"""Starting point for simulation"""

from typing import List, Dict
from container import PriorityQueue
from dispatcher import Dispatcher
from event import Event, create_event_list
from monitor import Monitor


class Simulation:
    """A simulation.

    This is the class that is responsible for setting up and running a
    simulation.

    The API is given to you: your main task is to implement the run
    method below according to its docstring.

    Of course, you may add whatever private attributes and methods you want.
    But because you should not change the interface, you may not add any public
    attributes or methods.

    This is the entry point into your program, and in particular is used for
    auto-testing purposes. This makes it ESSENTIAL that you do not change the
    interface in any way!
    """

    # === Private Attributes ===
    _events: PriorityQueue
    #     A sequence of events arranged in priority determined by the event
    #     sorting order.
    _dispatcher: Dispatcher
    #     The dispatcher associated with the simulation.
    _monitor: Monitor
    #     The monitor associated with the simulation.

    def __init__(self) -> None:
        """Initialize a Simulation.

        """
        self._events = PriorityQueue()
        self._dispatcher = Dispatcher()
        self._monitor = Monitor()

    def run(self, initial_events: List[Event]) -> Dict[str, float]:
        """Run the simulation on the list of events in <initial_events>.

        Return a dictionary containing statistics of the simulation,
        according to the specifications in the assignment handout.

        initial_events: An initial list of events.
        """
        for event in initial_events:
            self._events.add(event)
            print(f"Added event to queue: {event}")
        # print(str(self._events._items))

        while not self._events.is_empty():
            event = self._events.remove()
            print(f"Processing event: {event}")
            possible = event.do(self._dispatcher, self._monitor)
            for even in possible:
                self._events.add(even)
                # print(f"Added new event to queue: {even}")

        # Add all initial events to the event queue.

        # Until there are no more events, remove an event
        # from the event queue and do it. Add any returned
        # events to the event queue.

        return self._monitor.report()


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(
        config={
            'extra-imports': ['typing', 'container', 'dispatcher', 'event',
                              'monitor']})

    events = create_event_list("checking_samples")
    sim = Simulation()
    final_stats = sim.run(events)
    print(final_stats)

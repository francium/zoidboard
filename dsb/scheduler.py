from collections import namedtuple
import heapq as hq


"""
:param next_run: The next time this item is scheduled for (seconds since epoch)
:type next_run: Union[Int, Float]
"""
ScheduleItem = namedtuple('ScheduleItem', ['next_run', 'item'])


class Scheduler:
    def __init__(self, items=[]):
        """
        :param items: Mutable list of items that will be used to represent a
          sorted heap
        """
        self._heap = items
        hq.heapify(items)

    def peek_next(self):
        """See the next scheduled item without removing it from the scheduler
        """
        return hq.nsmallest(1, self._heap)[0]

    def get_next(self):
        """Get the next scheduled item and remove it from the scheduler
        """
        return hq.heappop(self._heap)

    def push(self, item: ScheduleItem):
        """Add an item to the scheduler
        """
        hq.heappush(self._heap, item)
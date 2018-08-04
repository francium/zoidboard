from typing import List

from dsb.scheduler import ScheduleItem, Scheduler


class TestScheduler:
    def _sample_schedule_items(self) -> List[ScheduleItem]:
        return [
            ScheduleItem(10, 10),
            ScheduleItem(11, 11),
            ScheduleItem(7, 7),
            ScheduleItem(15, 15),
        ]

    def test_scheduler_can_init(self):
        items = self._sample_schedule_items()
        s = Scheduler(items[:])
        assert len(s._heap) == 4, "Heap has been created"
        assert s._heap[0] == items[2], "Heap has been created and is sorted"

    def test_scheduler_peak_next_returns_smallest(self):
        items = self._sample_schedule_items()
        s = Scheduler(items[:])
        assert s.peek_next() == items[2]
        assert len(s._heap) == 4, "Heap has not gotten smaller"

    def test_scheduler_get_next_returns_smallest(self):
        items = self._sample_schedule_items()
        s = Scheduler(items[:])
        assert s.get_next() == items[2]
        assert len(s._heap) == 3, "Heap has gotten smaller"

    def test_scheduler_can_push_item(self):
        items = self._sample_schedule_items()
        new_item = ScheduleItem(9, 9)
        s = Scheduler(items)
        s.push(new_item)
        assert len(s._heap) == 5, "Heap has gotten bigger"
        s.get_next()
        assert s.get_next() == new_item, "New item was the second smallest in the heap"
from routine import Routine, test_routine
from typing import Iterable, List
from threading import Thread
from time import sleep
from collections import deque
import bisect
from datetime import datetime, time

class RoutineQueue(deque):
    """
    RoutineQueue is a deque that's been extended a bit to handle sorting and inserting the routines.
    Use insert_queue() in order to insert into the RoutineQueue. This will ensure that the queue remains sorted.
    """
    def __init__(self, iter: Iterable = None):
        super().__init__(iter)

    # Example of sorting deques with datetime.
    # https://stackoverflow.com/questions/19795642/how-to-sort-class-on-datetime-sort-collections-deque
    # Probably won't need to use this? But I think it would be handy to have around.
    def sort(self):
        items = [self.pop() for _ in range(len(self))]
        items.sort()
        self.extend(items)

    def insert_queue(self, routine):
        # This is with the assumption that the deque is already sorted.
        routines = [routine for routine in self]
        idx = bisect.bisect(routines, routine)
        self.insert(idx, routine)

class Scheduler:
    """
    Scheduler will run threads to check the queue and execute tasks.
    Scheduler will also manage the state of the routines and provides functions to add, delete, or edit routines.
    """
    def __init__(self, routine_list = List[Routine]):
        self.routine_queue = RoutineQueue()
        self.routines = {routine.name: routine for routine in routine_list}

    def _check_routine_queue(self):
        while True:
            print("Checking task queue...")
            print(f"{self.routine_queue=}")
            if self.routine_queue:
                self.execute_routine(self.routine_queue.popleft())
            sleep(5)

    def start_check_routine_queue(self):
        thread = Thread(target=self._check_routine_queue, name="Check Task Queue")
        thread.start()

    def _execute_routine(self):
        pass

    def execute_routine(self, name):
        thread = Thread(target=self._execute_routine, name=f"Task {name}", args=[name])
        thread.start()

    # We need to update the queue whenever we add, delete, or edit routines.

    def enqueue_routines(self):

        pass

    def add_routine(self, routine):
        """
        Add routine will either extend an existing routine or add a new entry into the 'routines' dict.
        """
        pass


if __name__ == "__main__":

    s = Scheduler()

    pass
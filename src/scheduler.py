from routine import Routine
from typing import List
import threading
import queue

class TaskQueue:
    """
    Manages the queue of tasks.
    """
    def __init__(self) -> None:
        pass

class Scheduler:
    def __init__(self, routines: List[Routine]):
        self.task_queue = []

    def _check_task_queue(self):
        while True:
            if self.task_queue[0]:
                pass

    def _execute_task(self, func):
        pass




if __name__ == "__main__":
    pass
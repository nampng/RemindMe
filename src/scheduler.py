from datetime import date
from routine import Routine
from threading import Thread, ThreadError
from time import sleep

class Scheduler():
    """
    Scheduler does two things:
    Manages the time table:

    Manages starting / stopping routines:

    """
    def __init__(self, time_table: dict = {}) -> None:
        self.time_table = time_table
        self._start()

    @classmethod
    def from_routine_list(cls, routines) -> "Scheduler":
        time_table = {}

        for routine in routines:
            if routine.day not in time_table:
                time_table[routine.day] = {}

            time_table[routine.day][routine.name] = routine

        return cls(time_table=time_table)

    def add(self, routine: Routine):
        if self.time_table[routine.day][routine.name]:
            print("Routine already exists.")
            return

        if routine.day not in self.time_table:
            self.time_table[routine.day] = set()

        self.time_table[routine.day][routine.name] = routine

    def update(self, routine: Routine):
        self.time_table[routine.day][routine.name].stop()
        self.time_table[routine.day][routine.name] = routine

    def remove(self, routine: Routine):
        try:
            self.time_table[routine.day][routine.name].stop()
            del self.time_table[routine.day][routine.name]
        except KeyError:
            print("Routine doesn't exist.")
        except ThreadError:
            print("Thread does not exist or is not alive.")

    def _start(self):
        """
        This starts the thread that will check routines and start / stop them when needed.
        """
        print("Starting scheduler...")
        Thread(target=self._check_routines, name="Scheduler").start()

    def _check_routines(self):
        while True:
            print("Checking for existing routines today...")
            if self.time_table[date.weekday()]:
                pass
            else:
                print("No routines today at this moment.")

            sleep(10)


if __name__ == "__main__":
    print("Scheduler.py")

    from datetime import time
    from routine import test_routine

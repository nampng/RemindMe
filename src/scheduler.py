from datetime import date, datetime
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
        # self._start()

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

    def remove(self, day: int, name: str):
        try:
            self.time_table[day][name].stop()
            del self.time_table[day][name]
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
            print("Checking...")
            now = datetime.now()
            if not self.time_table[now.weekday()]:
                print("No routines today at this moment.")
                return

            routine: Routine # Cool typing, wow. Wanted this here so that intellisense worked below.
            for routine in self.time_table[now.weekday()].values():
                if routine.thread and (routine.thread.is_alive() or routine.remind_me):
                    continue

                if now.time() <= routine.target_time:
                    routine.start()

            sleep(1)

    def get_reminders(self):
        now = datetime.now().weekday()
        if now in self.time_table:
            return [routine for routine in self.time_table[now].values() if routine.remind_me]

    def clear_reminder(self, day: int, name: str):
        self.time_table[day][name].remind_me = False

if __name__ == "__main__":
    print("Scheduler.py")
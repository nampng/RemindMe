from datetime import datetime
from typing import List, Tuple
from routine import Routine
from threading import Thread, ThreadError
from time import sleep

class Scheduler():
    """
    Scheduler mainly does two things:
    
    Manages the time table:
    
    The time table is a dictionary that looks like this:
    {day: {name: routine}} where day is an int representing the day of the week, 
    name is a str that identifies the routine, and routine is a Routine object.

    The scheduler can add, delete, and update keys/values in the time table.

    Checks routines:
    
    The scheduler will start a thread which runs the function _check_routines(). 
    This function checks if there are any existing routines today 
    and will run the routines if reminders for them haven't been triggered yet 
    and the current time is before the routine's target time.
    """
    def __init__(self, time_table: dict = {}) -> None:
        self.time_table = time_table
        self._start()

    @classmethod
    def from_routine_list(cls, routines) -> "Scheduler":
        """
        In case we have a list of existing routines, we can create time table out of them with this class method.
        """
        time_table = {}

        for routine in routines:
            if routine.day not in time_table:
                time_table[routine.day] = {}

            time_table[routine.day][routine.name] = routine

        return cls(time_table=time_table)

    def add(self, name, day, target_time, description) -> None:
        """
        Adds a new routine into the time table.

        You cannot add a routine that's already existing. 
        Use update() for that.
        """
        routine = Routine(name=name, day=day, target_time=target_time, description=description)
        if day in self.time_table and name in self.time_table[day]:
            print("Routine already exists.")
            return

        if routine.day not in self.time_table:
            self.time_table[routine.day] = {}

        self.time_table[routine.day][routine.name] = routine

    def update(self, name, day, target_time, description) -> None:
        """
        Updates an existing routine. 
        Will stop the current routine from running, if it is, and replace the old routine with the new routine.
        """
        routine = Routine(name=name, day=day, target_time=target_time, description=description)

        try:
            self.time_table[day][name].stop()
        except ThreadError:
            print("Thread does not exist or is not alive.")

        self.time_table[day][name] = routine

    def remove(self, day: int, name: str) -> None:
        """
        Removes a routine from the time table.

        Will attempt to stop the routine first, then it will delete the key to the routine in the time table.
        """
        try:
            try:
                self.time_table[day][name].stop()
            except ThreadError:
                print("Thread does not exist or is not alive.")

            del self.time_table[day][name]
        except KeyError:
            print("Routine doesn't exist.")

    def _start(self) -> None:
        """
        This starts the thread that will check routines and start / stop them when needed.
        """
        print("Starting scheduler...")
        Thread(target=self._check_routines, name="Scheduler").start()

    def _check_routines(self) -> None:
        """
        Checks if there are routines that need to be run every second.
        """
        while True:
            now = datetime.now()

            print(f"Current time is {now.time()}. Checking routines...")

            if now.weekday() not in self.time_table:
                print("No routines today at this moment.")
            else:
                routine: Routine # Cool typing, wow. Wanted this here so that intellisense worked below.
                for routine in self.time_table[now.weekday()].values():
                    if routine.check_thread() or routine.has_reminder():
                        continue

                    if now.time() <= routine.target_time:
                        routine.start()

            sleep(1)

    def get_reminders(self) -> List[Tuple]:
        """
        Returns a list of tuples consisting of (routine.name, routine.description).
        """
        now = datetime.now().weekday()
        if now in self.time_table:
            return [(routine.name, routine.description) for routine in self.time_table[now].values() if routine.has_reminder()]

    def clear_reminder(self, day: int, name: str) -> None:
        """
        Calls the clear_reminder() function for the desired routine.
        """
        self.time_table[day][name].clear_reminder()

if __name__ == "__main__":
    print("Scheduler.py")
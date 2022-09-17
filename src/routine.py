from datetime import time, datetime
from dataclasses import dataclass, field
from threading import Thread, ThreadError
from time import sleep

@dataclass
class Routine:
    """
    Routine class holds information about a particular routine as well as functions to
    set the state of the routine.
    """
    name: str
    day: int
    target_time: time
    description: str = field(repr=False, default="")
    _remind_me: bool = field(repr=False, default=False) 
    _force_stop: bool = field(repr=False, default=False) 
    _thread: Thread = field(repr=False, default=None) 
    
    def start(self):
        """
        Starts a thread that runs self._wait_for_day_time
        Will reset the remind_me variable to False.
        """
        if self._force_stop:
            # Since every second we may be trying to start a thread, if routine needs to be stopped
            # it would be troublesome to have a routine start the same moment we're trying to remove it.
            # So prevent it from running in the first place if force_stop == True.
            return

        self._remind_me = False

        t = Thread(target=self._wait_for_day_time, name=f"{self.name}")
        self._thread = t
        self._thread.start()

    def stop(self):
        """
        Force stops will be needed when a routine is being removed or updated.
        This is because the thread will still run even if the reference to it is removed.
        """
        if self.check_thread():
            self._force_stop = True
        else:
            raise ThreadError

    def _wait_for_day_time(self):
        """
        Waits for the set day and time. 
        
        Will die once the current time meets the target_time or exceeds it. It will set remind_me to True.

        There is an option to force stop the thread, in the case that the routine needs
        to be removed or updated.
        """
        while True:
            if self._force_stop:
                print("Force stopping...")
                self._force_stop = False
                break

            now = datetime.now()
            if now.weekday() == self.day and now.time() >= self.target_time:
                print(f"Triggering reminder for {self.name}")
                self._remind_me = True
                break

            print(f"Waiting for trigger for {self.name}")
            sleep(1)
    
    def clear_reminder(self):
        """
        Sets _remind_me to False which will exclude it from the reminder list given by Scheduler.
        
        Also sets _thread to None, since it won't be needed anymore.
        """
        self._remind_me = False

        try:
            self.stop()
        except ThreadError:
            print("No thread to stop or already stopped.")

        self._thread = None # Might as well clear the thread too if we're clearing the reminder. A new one will be created later.

    def has_reminder(self) -> bool:
        """
        Returns _remind_me. 
        """
        return self._remind_me

    def check_thread(self) -> bool:
        """
        Returns True if the thread is not None and is alive.
        
        Returns False otherwise.
        """
        return self._thread and self._thread.is_alive()
    
# Use this for testing purposes.
test_routine = Routine(name="test", description="test", day=1, target_time=time(hour=1))

if __name__ == "__main__":
    print("Routine.py")

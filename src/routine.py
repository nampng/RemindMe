from typing import List, Tuple
from datetime import time, datetime

class Point:
    def __init__(self, day: int, time_period: time) -> None:
        self.point = (day, time_period)

    @classmethod
    def from_str(cls, string: str):
        pass

    @classmethod
    def from_datetime(cls, obj: datetime):
        pass

    def __iter__(self) -> Tuple[int, time]:
        return iter(self.point)

class TimeTable(dict):
    def __init__(self, points: List[Point]) -> None:
        self.time_table = self.create_time_table(points)
        super().__init__(self.time_table)

    @staticmethod
    def create_time_table(points):
        time_table = {}

        for point in points:
            day, time_period = point

            if day not in time_table:
                time_table[day] = set()

            time_table[day].add(time_period)

        return time_table


class Routine:
    def __init__(self, name: str, time_table: TimeTable, freq: int = 1, forever: bool = False) -> None:
        """
        Args
        name: Routine name
        time_table: TimeTable obj representing points in time in a week
        freq: Frequency in which the routine will trigger, will decrement every time routine runs (0 will never run)
        forever: If forever == True then freq will never decrement
        """

        self.name = name
        self.time_table = time_table
        self.freq = freq
        self.forever = forever

    def add_time_table(self, new_time_table):
        """
        Merges a new time table into the existing time table.
        """
        for key in new_time_table:
            if (time_set := self.time_table.get(key)):
                self.time_table[key] = time_set | new_time_table[key] # set merge
            else:
                self.time_table[key] = new_time_table[key]

    def decrement_freq(self):
        if not self.forever:
            self.freq -= 1

if __name__ == "__main__":
    print(__name__)



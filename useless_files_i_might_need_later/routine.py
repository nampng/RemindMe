class TimeTable(dict):
    """
    TimeTable creates a map where the keys are the days of the week (0 - 6) and the
    values are the associated times for those days.

    
    """
    def __init__(self, routines) -> None:
        self.time_table = self.create_time_table(routines)
        super().__init__(self.time_table)

    def create_time_table(self, routines):
        time_table = {}

        for routine in routines:
            day, target_time = routine.day, routine.target_time

            if day not in time_table:
                time_table[day] = {}

            time_table[day][target_time] = None

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
from datetime import time
from ..src.routine import Routine

def test_make_point():
    point = Point(day=0, time_period=time(hour=1))
    day, time_period = point

    assert point.point == (0, time(hour=1))
    assert day == 0 and time_period == time(hour=1)

def test_make_time_table():
    points = [Point(1, time(hour=1)), Point(2, time(hour=2))]
    time_table = TimeTable(points)

    assert time(hour=1) in time_table[1]
    assert time(hour=2) in time_table[2]

def test_make_routine():
    points = [Point(1, time(hour=1)), Point(2, time(hour=2))]
    time_table = TimeTable(points)

    routine = Routine(name="test", time_table=time_table)

    assert routine.time_table == time_table
    assert routine.freq == 1
    assert routine.forever == False

def test_routine_freq_decrement():
    points = [Point(1, time(hour=1)), Point(2, time(hour=2))]
    time_table = TimeTable(points)

    routine = Routine(name="test", time_table=time_table)

    routine.decrement_freq()

    assert routine.freq == 0

def test_routine_forever_freq():
    points = [Point(1, time(hour=1)), Point(2, time(hour=2))]
    time_table = TimeTable(points)

    routine = Routine(name="test", time_table=time_table, forever=True)

    routine.decrement_freq()

    assert routine.freq == 1

def test_update_routine_time_table():
    points = [Point(1, time(hour=1)), Point(2, time(hour=2))]
    time_table = TimeTable(points)

    points2 = [Point(1, time(hour=2)), Point(5, time(hour=5))]
    time_table2 = TimeTable(points2)

    routine = Routine(name="test", time_table=time_table)

    routine.add_time_table(time_table2)

    assert 5 in routine.time_table
    assert set([time(hour=1), time(hour=2)]) == routine.time_table[1]
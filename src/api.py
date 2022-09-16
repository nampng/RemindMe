from fastapi import FastAPI
from routine import Routine
from scheduler import Scheduler
from pydantic import BaseModel
from datetime import time
import json

class RoutineData(BaseModel):
    name: str
    day: int
    target_time: time
    description: str = ""

app = FastAPI()
scheduler = Scheduler()

# https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
class TimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, time):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

@app.get("/")
def root():
    """
    This returns a list of routines that have remind_me == True
    """
    return "Hello, world"

@app.post("/add")
def add_routine(data: RoutineData):
    pass

@app.post("/remove")
def remove_routine(data: RoutineData):
    pass

@app.post("/update")
def update_routine(data: RoutineData):
    pass

def clear_reminder(data: RoutineData):
    pass


if __name__ == "__main__":
    t = time(hour=1)
    j = json.dumps(obj=t, cls=TimeEncoder)
    j = json.loads(j)
    t2 = time.fromisoformat(j)
    print(t)
    print(t2)
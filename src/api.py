from fastapi import FastAPI
from routine import Routine
from scheduler import Scheduler
from pydantic import BaseModel
from datetime import time
import json

class RoutineData(BaseModel):
    name: str
    day: int
    target_time: str | None
    description: str = ""

    def __iter__(self):
        return iter((self.name, self.day, self.target_time, self.description))

class Response(BaseModel):
    msg: str
    data: str | None

app = FastAPI()
scheduler = Scheduler()

# https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
class TimeEncoder(json.JSONEncoder):
    """
    This is to convert time to str in json.dumps(). Probably won't need this since I'll just do
    time.isoformat() and pass into json.dumps(), but maybe I'll need it later on for something else.
    If not, this will be banished to the useless_files folder.
    """
    def default(self, o):
        if isinstance(o, time):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

@app.get("/")
def root() -> Response:
    """
    This returns a list of routines that have remind_me == True
    """
    reminders = scheduler.get_reminders()
    return Response(msg=f"{len(reminders) if reminders else 0} reminders retrieved.", data=json.dumps(reminders))

@app.post("/add")
def add_routine(data: RoutineData) -> Response:
    name, day, target_time, description = data
    scheduler.add(
        name=name, 
        day=day, 
        target_time=time.fromisoformat(target_time), 
        description=description
        )
    return Response(msg=f"Routine '{name}' added.")

@app.post("/remove")
def remove_routine(data: RoutineData) -> Response:
    name, day, *_ = data
    scheduler.remove(name=name, day=day)
    return Response(msg=f"Routine '{name}' removed.")

@app.post("/update")
def update_routine(data: RoutineData) -> Response:
    name, day, target_time, description = data
    scheduler.update(
        name=name, 
        day=day, 
        target_time=time.fromisoformat(target_time), 
        description=description)
    return Response(msg=f"Routine '{name}' updated.")

@app.post("/clear")
def clear_reminder(data: RoutineData) -> Response:
    name, day, *_ = data
    scheduler.clear_reminder(name=name, day=day)
    return Response(msg=f"Cleared reminder for {name}.")


if __name__ == "__main__":
    from datetime import datetime
    print(datetime.now().time())
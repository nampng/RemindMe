from fastapi import FastAPI
from routine import Routine
from scheduler import Scheduler

app = FastAPI()
scheduler = Scheduler()
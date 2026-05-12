from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import init_db
from .frontend import router as frontend_router
from .admin import router as admin_router

app = FastAPI(title="Panchnad Shodh Sansthan")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(frontend_router)
app.include_router(admin_router, prefix="/admin")

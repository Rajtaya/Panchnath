import os
from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session

# Use /data volume on Railway, local file otherwise
DATA_DIR = Path(os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", "."))
DB_PATH = DATA_DIR / "panchnad.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

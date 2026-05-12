from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from .database import init_db, engine
from .models import AdminUser
from .frontend import router as frontend_router
from .admin import router as admin_router

app = FastAPI(title="Panchnad Shodh Sansthan")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
def on_startup():
    init_db()
    # Auto-seed if DB is empty (first deploy)
    with Session(engine) as s:
        if not s.exec(select(AdminUser)).first():
            _seed(s)


def _seed(s: Session):
    """Seed initial data on first run."""
    from datetime import date
    from .models import Centre, Post, Person, Publication, AnnualLecture, GalleryImage
    from .auth import hash_password

    s.add(AdminUser(username="admin", password_hash=hash_password("panchnad2025")))

    for c in [
        Centre(name="Panchnad Adhyayan Kendra", location="Panjab University, Chandigarh"),
        Centre(name="Panchnad Adhyayan Kendra", location="Chandigarh"),
        Centre(name="Panchnad Adhyayan Kendra", location="Hisar, Haryana"),
        Centre(name="Panchnad Adhyayan Kendra", location="Kurukshetra, Haryana"),
        Centre(name="Panchnad Adhyayan Kendra", location="Solan, Himachal Pradesh"),
        Centre(name="Adhyayan Kendra", location="Himachal Pradesh University, Shimla"),
    ]:
        s.add(c)

    s.add(Person(name="Prof. Brij Kishore Kuthiala", role="President (Adhyaksh), Panchnad Shodh Sansthan",
        bio="Born 1948. Chairman of Haryana State Higher Education Council. Former Vice-Chancellor, Makhanlal Chaturvedi National University. Over 51 years in media teaching and academic management."))
    s.add(Person(name="Justice T. U. Mehta", role="Founding Chairman (1984)",
        bio="Former Chief Justice of Himachal Pradesh High Court. Founded Panchnad Research Institute in 1984."))

    posts_data = [
        ("31st Annual Panchnad Lecture — Truth of Partition of India",
         "31st Annual Panchnad Lecture. Chief Guest: Punjab Governor Gulab Chand Kataria. Speaker: Prashant Paul. Books released: Vichar Pravah & Human Values and Rights in Quran.",
         date(2025, 1, 5), "Annual Lecture"),
    ]
    for title, body, d, tag in posts_data:
        s.add(Post(title=title, body=body, posted_on=d, tag=tag))

    pubs = [
        ("Vichar Pravah", "Collection of thought essays. Released at 31st Annual Lecture.", 2025),
        ("Human Values and Rights in Quran", "Study on human values as expressed in the Quran.", 2025),
        ("Bharat 2047 — A Collective Vision", "Collective vision of 20 experts on culture, technology, economics.", 2022),
        ("Facts Speak for Themselves", "Field study report on 1984 anti-Sikh riots.", 1985),
    ]
    for title, desc, year in pubs:
        s.add(Publication(title=title, description=desc, year=year, author_or_editor="Panchnad Shodh Sansthan"))

    lectures_data = [
        (2025, "Prashant Paul", "Truth of Partition of India"),
        (2008, "Mohan Bhagwat", "National security and cultural issues"),
        (2005, "Devinder Swarup", "Contemporary national discourse"),
        (2003, "Arun Jaitley", "Constitutional law and governance"),
        (2001, "K. P. S. Gill", "Internal security challenges"),
        (1999, "K. N. Govindacharya", "Socio-political thought"),
        (1997, "Samdong Rinpoche", "Tibetan culture and Indian heritage"),
        (1993, "Dr. M. M. Joshi", "Education and national identity"),
        (1990, "Justice D. S. Tewatia", "Judiciary and constitutional values"),
        (1987, "Lt. Gen. S. K. Sinha", "National security perspectives"),
    ]
    for year, speaker, topic in lectures_data:
        s.add(AnnualLecture(year=year, speaker=speaker, topic=topic))

    s.commit()


app.include_router(frontend_router)
app.include_router(admin_router, prefix="/admin")

from datetime import date
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from .database import get_session
from .models import Centre, Post, Person, Publication, AnnualLecture, GalleryImage, ContactInquiry

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request, session: Session = Depends(get_session)):
    posts = session.exec(select(Post).order_by(Post.posted_on.desc())).all()[:5]
    centres_count = len(session.exec(select(Centre)).all())
    lectures_count = len(session.exec(select(AnnualLecture)).all())
    return templates.TemplateResponse("index.html", {
        "request": request,
        "posts": posts,
        "centres_count": centres_count,
        "lectures_count": lectures_count,
    })


@router.get("/about", response_class=HTMLResponse)
def about(request: Request, session: Session = Depends(get_session)):
    people = session.exec(select(Person)).all()
    return templates.TemplateResponse("about.html", {"request": request, "people": people})


@router.get("/posts", response_class=HTMLResponse)
def posts_page(request: Request, q: str = "", session: Session = Depends(get_session)):
    items = session.exec(select(Post).order_by(Post.posted_on.desc())).all()
    if q:
        ql = q.lower()
        items = [p for p in items if ql in p.title.lower() or ql in p.body.lower()]
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse("_posts_list.html", {"request": request, "posts": items})
    return templates.TemplateResponse("posts.html", {"request": request, "posts": items, "q": q})


@router.get("/centres", response_class=HTMLResponse)
def centres(request: Request, session: Session = Depends(get_session)):
    items = session.exec(select(Centre)).all()
    return templates.TemplateResponse("centres.html", {"request": request, "centres": items})


@router.get("/publications", response_class=HTMLResponse)
def publications(request: Request, session: Session = Depends(get_session)):
    pubs = session.exec(select(Publication).order_by(Publication.year.desc())).all()
    return templates.TemplateResponse("publications.html", {"request": request, "publications": pubs})


@router.get("/lectures", response_class=HTMLResponse)
def lectures(request: Request, session: Session = Depends(get_session)):
    items = session.exec(select(AnnualLecture).order_by(AnnualLecture.year.desc())).all()
    return templates.TemplateResponse("lectures.html", {"request": request, "lectures": items})


@router.get("/gallery", response_class=HTMLResponse)
def gallery(request: Request, session: Session = Depends(get_session)):
    images = session.exec(select(GalleryImage).order_by(GalleryImage.event_date.desc())).all()
    return templates.TemplateResponse("gallery.html", {"request": request, "images": images})


@router.get("/contact", response_class=HTMLResponse)
def contact(request: Request):
    msg = request.query_params.get("msg")
    return templates.TemplateResponse("contact.html", {"request": request, "msg": msg})


@router.post("/contact")
async def contact_submit(request: Request, session: Session = Depends(get_session)):
    form = await request.form()
    inquiry = ContactInquiry(
        name=form["name"],
        email=form["email"],
        subject=form["subject"],
        message=form["message"],
        submitted_on=date.today(),
    )
    session.add(inquiry)
    session.commit()
    return RedirectResponse("/contact?msg=sent", status_code=303)

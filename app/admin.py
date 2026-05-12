import os
import uuid
from datetime import date
from pathlib import Path
from fastapi import APIRouter, Request, Depends, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from .database import get_session
from .models import Centre, Post, Person, Publication, AnnualLecture, AdminUser, ContactInquiry, GalleryImage
from .auth import check_admin, verify_password, create_token

GALLERY_DIR = Path("app/static/gallery")

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ── Auth ──────────────────────────────────────────────────────────────

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    if check_admin(request):
        return RedirectResponse("/admin/dashboard", status_code=303)
    error = request.query_params.get("error")
    return templates.TemplateResponse("admin/login.html", {"request": request, "error": error})


@router.post("/login")
async def login(request: Request, session: Session = Depends(get_session)):
    form = await request.form()
    user = session.exec(select(AdminUser).where(AdminUser.username == form["username"])).first()
    if not user or not verify_password(form["password"], user.password_hash):
        return RedirectResponse("/admin/login?error=1", status_code=303)
    token = create_token(user.username)
    response = RedirectResponse("/admin/dashboard", status_code=303)
    response.set_cookie("admin_session", token, httponly=True, max_age=86400)
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse("/admin/login", status_code=303)
    response.delete_cookie("admin_session")
    return response


# ── Dashboard ─────────────────────────────────────────────────────────

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    stats = {
        "posts": len(session.exec(select(Post)).all()),
        "publications": len(session.exec(select(Publication)).all()),
        "centres": len(session.exec(select(Centre)).all()),
        "lectures": len(session.exec(select(AnnualLecture)).all()),
        "people": len(session.exec(select(Person)).all()),
        "gallery": len(session.exec(select(GalleryImage)).all()),
        "inquiries": len(session.exec(select(ContactInquiry)).all()),
    }
    recent_posts = session.exec(select(Post).order_by(Post.posted_on.desc())).all()[:5]
    recent_inquiries = session.exec(select(ContactInquiry).order_by(ContactInquiry.submitted_on.desc())).all()[:5]
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request, "stats": stats,
        "recent_posts": recent_posts, "recent_inquiries": recent_inquiries,
    })


# ── Posts CRUD ────────────────────────────────────────────────────────

@router.get("/posts", response_class=HTMLResponse)
def admin_posts(request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    posts = session.exec(select(Post).order_by(Post.posted_on.desc())).all()
    msg = request.query_params.get("msg")
    return templates.TemplateResponse("admin/posts.html", {"request": request, "posts": posts, "msg": msg})


@router.get("/posts/new", response_class=HTMLResponse)
def admin_post_new(request: Request):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    return templates.TemplateResponse("admin/post_form.html", {"request": request, "post": None})


@router.post("/posts/new")
async def admin_post_create(request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    form = await request.form()
    post = Post(
        title=form["title"], body=form["body"],
        posted_on=date.fromisoformat(form["posted_on"]),
        link=form.get("link") or None, tag=form.get("tag") or None,
    )
    session.add(post)
    session.commit()
    return RedirectResponse("/admin/posts?msg=created", status_code=303)


@router.get("/posts/{id}/edit", response_class=HTMLResponse)
def admin_post_edit(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    post = session.get(Post, id)
    return templates.TemplateResponse("admin/post_form.html", {"request": request, "post": post})


@router.post("/posts/{id}/edit")
async def admin_post_update(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    post = session.get(Post, id)
    form = await request.form()
    post.title = form["title"]
    post.body = form["body"]
    post.posted_on = date.fromisoformat(form["posted_on"])
    post.link = form.get("link") or None
    post.tag = form.get("tag") or None
    session.add(post)
    session.commit()
    return RedirectResponse("/admin/posts?msg=updated", status_code=303)


@router.post("/posts/{id}/delete")
def admin_post_delete(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    post = session.get(Post, id)
    session.delete(post)
    session.commit()
    return RedirectResponse("/admin/posts?msg=deleted", status_code=303)


# ── Publications CRUD ─────────────────────────────────────────────────

@router.get("/publications", response_class=HTMLResponse)
def admin_publications(request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    pubs = session.exec(select(Publication).order_by(Publication.year.desc())).all()
    msg = request.query_params.get("msg")
    return templates.TemplateResponse("admin/publications.html", {"request": request, "publications": pubs, "msg": msg})


@router.get("/publications/new", response_class=HTMLResponse)
def admin_pub_new(request: Request):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    return templates.TemplateResponse("admin/publication_form.html", {"request": request, "pub": None})


@router.post("/publications/new")
async def admin_pub_create(request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    form = await request.form()
    pub = Publication(
        title=form["title"], description=form["description"],
        year=int(form["year"]), author_or_editor=form.get("author_or_editor") or None,
    )
    session.add(pub)
    session.commit()
    return RedirectResponse("/admin/publications?msg=created", status_code=303)


@router.get("/publications/{id}/edit", response_class=HTMLResponse)
def admin_pub_edit(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    pub = session.get(Publication, id)
    return templates.TemplateResponse("admin/publication_form.html", {"request": request, "pub": pub})


@router.post("/publications/{id}/edit")
async def admin_pub_update(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    pub = session.get(Publication, id)
    form = await request.form()
    pub.title = form["title"]
    pub.description = form["description"]
    pub.year = int(form["year"])
    pub.author_or_editor = form.get("author_or_editor") or None
    session.add(pub)
    session.commit()
    return RedirectResponse("/admin/publications?msg=updated", status_code=303)


@router.post("/publications/{id}/delete")
def admin_pub_delete(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    pub = session.get(Publication, id)
    session.delete(pub)
    session.commit()
    return RedirectResponse("/admin/publications?msg=deleted", status_code=303)


# ── Centres CRUD ──────────────────────────────────────────────────────

@router.get("/centres", response_class=HTMLResponse)
def admin_centres(request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    items = session.exec(select(Centre)).all()
    msg = request.query_params.get("msg")
    return templates.TemplateResponse("admin/centres.html", {"request": request, "centres": items, "msg": msg})


@router.get("/centres/new", response_class=HTMLResponse)
def admin_centre_new(request: Request):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    return templates.TemplateResponse("admin/centre_form.html", {"request": request, "centre": None})


@router.post("/centres/new")
async def admin_centre_create(request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    form = await request.form()
    centre = Centre(name=form["name"], location=form["location"])
    session.add(centre)
    session.commit()
    return RedirectResponse("/admin/centres?msg=created", status_code=303)


@router.get("/centres/{id}/edit", response_class=HTMLResponse)
def admin_centre_edit(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    centre = session.get(Centre, id)
    return templates.TemplateResponse("admin/centre_form.html", {"request": request, "centre": centre})


@router.post("/centres/{id}/edit")
async def admin_centre_update(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    centre = session.get(Centre, id)
    form = await request.form()
    centre.name = form["name"]
    centre.location = form["location"]
    session.add(centre)
    session.commit()
    return RedirectResponse("/admin/centres?msg=updated", status_code=303)


@router.post("/centres/{id}/delete")
def admin_centre_delete(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    centre = session.get(Centre, id)
    session.delete(centre)
    session.commit()
    return RedirectResponse("/admin/centres?msg=deleted", status_code=303)


# ── Lectures CRUD ─────────────────────────────────────────────────────

@router.get("/lectures", response_class=HTMLResponse)
def admin_lectures(request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    items = session.exec(select(AnnualLecture).order_by(AnnualLecture.year.desc())).all()
    msg = request.query_params.get("msg")
    return templates.TemplateResponse("admin/lectures.html", {"request": request, "lectures": items, "msg": msg})


@router.get("/lectures/new", response_class=HTMLResponse)
def admin_lecture_new(request: Request):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    return templates.TemplateResponse("admin/lecture_form.html", {"request": request, "lecture": None})


@router.post("/lectures/new")
async def admin_lecture_create(request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    form = await request.form()
    lec = AnnualLecture(year=int(form["year"]), speaker=form["speaker"], topic=form.get("topic") or None)
    session.add(lec)
    session.commit()
    return RedirectResponse("/admin/lectures?msg=created", status_code=303)


@router.get("/lectures/{id}/edit", response_class=HTMLResponse)
def admin_lecture_edit(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    lec = session.get(AnnualLecture, id)
    return templates.TemplateResponse("admin/lecture_form.html", {"request": request, "lecture": lec})


@router.post("/lectures/{id}/edit")
async def admin_lecture_update(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    lec = session.get(AnnualLecture, id)
    form = await request.form()
    lec.year = int(form["year"])
    lec.speaker = form["speaker"]
    lec.topic = form.get("topic") or None
    session.add(lec)
    session.commit()
    return RedirectResponse("/admin/lectures?msg=updated", status_code=303)


@router.post("/lectures/{id}/delete")
def admin_lecture_delete(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    lec = session.get(AnnualLecture, id)
    session.delete(lec)
    session.commit()
    return RedirectResponse("/admin/lectures?msg=deleted", status_code=303)


# ── People CRUD ───────────────────────────────────────────────────────

@router.get("/people", response_class=HTMLResponse)
def admin_people(request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    items = session.exec(select(Person)).all()
    msg = request.query_params.get("msg")
    return templates.TemplateResponse("admin/people.html", {"request": request, "people": items, "msg": msg})


@router.get("/people/new", response_class=HTMLResponse)
def admin_person_new(request: Request):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    return templates.TemplateResponse("admin/person_form.html", {"request": request, "person": None})


@router.post("/people/new")
async def admin_person_create(request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    form = await request.form()
    person = Person(name=form["name"], role=form["role"], bio=form.get("bio") or None)
    session.add(person)
    session.commit()
    return RedirectResponse("/admin/people?msg=created", status_code=303)


@router.get("/people/{id}/edit", response_class=HTMLResponse)
def admin_person_edit(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    person = session.get(Person, id)
    return templates.TemplateResponse("admin/person_form.html", {"request": request, "person": person})


@router.post("/people/{id}/edit")
async def admin_person_update(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    person = session.get(Person, id)
    form = await request.form()
    person.name = form["name"]
    person.role = form["role"]
    person.bio = form.get("bio") or None
    session.add(person)
    session.commit()
    return RedirectResponse("/admin/people?msg=updated", status_code=303)


@router.post("/people/{id}/delete")
def admin_person_delete(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    person = session.get(Person, id)
    session.delete(person)
    session.commit()
    return RedirectResponse("/admin/people?msg=deleted", status_code=303)


# ── Gallery CRUD ─────────────────────────────────────────────────────

@router.get("/gallery", response_class=HTMLResponse)
def admin_gallery(request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    images = session.exec(select(GalleryImage).order_by(GalleryImage.event_date.desc())).all()
    msg = request.query_params.get("msg")
    return templates.TemplateResponse("admin/gallery.html", {"request": request, "images": images, "msg": msg})


@router.get("/gallery/new", response_class=HTMLResponse)
def admin_gallery_new(request: Request):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    return templates.TemplateResponse("admin/gallery_form.html", {"request": request, "image": None})


@router.post("/gallery/new")
async def admin_gallery_create(request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    form = await request.form()
    file: UploadFile = form["image_file"]
    ext = Path(file.filename).suffix or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    GALLERY_DIR.mkdir(parents=True, exist_ok=True)
    with open(GALLERY_DIR / filename, "wb") as f:
        f.write(await file.read())
    img = GalleryImage(
        title=form["title"],
        description=form.get("description") or None,
        event_date=date.fromisoformat(form["event_date"]),
        image_filename=filename,
        centre=form.get("centre") or None,
    )
    session.add(img)
    session.commit()
    return RedirectResponse("/admin/gallery?msg=created", status_code=303)


@router.get("/gallery/{id}/edit", response_class=HTMLResponse)
def admin_gallery_edit(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    image = session.get(GalleryImage, id)
    return templates.TemplateResponse("admin/gallery_form.html", {"request": request, "image": image})


@router.post("/gallery/{id}/edit")
async def admin_gallery_update(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    image = session.get(GalleryImage, id)
    form = await request.form()
    image.title = form["title"]
    image.description = form.get("description") or None
    image.event_date = date.fromisoformat(form["event_date"])
    image.centre = form.get("centre") or None
    file: UploadFile = form.get("image_file")
    if file and file.filename:
        old_path = GALLERY_DIR / image.image_filename
        if old_path.exists():
            old_path.unlink()
        ext = Path(file.filename).suffix or ".jpg"
        filename = f"{uuid.uuid4().hex}{ext}"
        with open(GALLERY_DIR / filename, "wb") as f:
            f.write(await file.read())
        image.image_filename = filename
    session.add(image)
    session.commit()
    return RedirectResponse("/admin/gallery?msg=updated", status_code=303)


@router.post("/gallery/{id}/delete")
def admin_gallery_delete(id: int, request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    image = session.get(GalleryImage, id)
    file_path = GALLERY_DIR / image.image_filename
    if file_path.exists():
        file_path.unlink()
    session.delete(image)
    session.commit()
    return RedirectResponse("/admin/gallery?msg=deleted", status_code=303)


# ── Inquiries (read-only) ────────────────────────────────────────────

@router.get("/inquiries", response_class=HTMLResponse)
def admin_inquiries(request: Request, session: Session = Depends(get_session)):
    if not check_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    items = session.exec(select(ContactInquiry).order_by(ContactInquiry.submitted_on.desc())).all()
    return templates.TemplateResponse("admin/inquiries.html", {"request": request, "inquiries": items})

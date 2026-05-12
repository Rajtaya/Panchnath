from __future__ import annotations
from datetime import date
from sqlmodel import SQLModel, Field


class Centre(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    location: str


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    body: str
    posted_on: date
    link: str | None = None
    tag: str | None = None


class Person(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    role: str
    bio: str | None = None


class Publication(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    year: int
    author_or_editor: str | None = None


class AnnualLecture(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    year: int
    speaker: str
    topic: str | None = None


class AdminUser(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password_hash: str


class GalleryImage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = None
    event_date: date
    image_filename: str
    centre: str | None = None


class ContactInquiry(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    subject: str
    message: str
    submitted_on: date

from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field


class Source(BaseModel):
    id: str
    name: str


class Article(BaseModel):
    source: Source
    author: str | None = None
    title: str | None = None
    description: str | None = None
    url: str | None = None
    url_to_image: str | None = Field(..., alias="urlToImage")
    published_at: datetime = Field(..., alias="publishedAt")
    content: str | None = None

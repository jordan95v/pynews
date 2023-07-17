from datetime import datetime
from pydantic import BaseModel, Field, field_validator

AVAILABLE_LANGUAGES: list[str] = [
    "ar",
    "de",
    "en",
    "es",
    "fr",
    "he",
    "it",
    "nl",
    "no",
    "pt",
    "ru",
    "se",
    "ud",
    "zh",
]


class Search(BaseModel):
    q: str
    sources: str | None = None
    page: int | None = None
    page_size: int | None = Field(None, alias="pageSize")


class SearchEverything(Search):
    search_in: str | None = Field(None, alias="searchIn")
    exclude_domains: str | None = Field(None, alias="excludeDomains")
    from_date: datetime | None = Field(None, alias="from")
    to_date: datetime | None = Field(None, alias="to")
    sort_by: str | None = Field(None, alias="sortBy")
    domains: str | None = None
    language: str | None = None

    class Config:
        populate_by_name = True

    @field_validator("search_in")
    def search_in_available_value(cls, value: str):
        if value not in ["title", "description", "content"]:
            raise ValueError("search_in must be one of title, description, content")
        return value

    @field_validator("sort_by")
    def sort_by_available_value(cls, value: str):
        if value not in ["relevancy", "popularity", "publishedAt"]:
            raise ValueError(
                "sort_by must be one of relevancy, popularity, publishedAt"
            )
        return value

    @field_validator("language")
    def language_available_value(cls, value: str):
        if value not in AVAILABLE_LANGUAGES:
            raise ValueError(
                f"language must be one of {', '.join(AVAILABLE_LANGUAGES)}"
            )
        return value

from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class SearchEverything(BaseModel):
    q: str
    search_in: str | None = Field(None, alias="searchIn")
    exclude_domains: str | None = Field(None, alias="excludeDomains")
    from_date: datetime | None = Field(None, alias="from")
    to_date: datetime | None = Field(None, alias="to")
    sort_by: str | None = Field(None, alias="sortBy")
    page_size: int | None = Field(None, alias="pageSize")
    sources: str | None = None
    domains: str | None = None
    language: str | None = None
    page: int | None = None

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

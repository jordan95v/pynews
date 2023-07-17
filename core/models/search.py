from datetime import datetime
from typing import Any
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

AVAILABLE_CATEGORY: list[str] = [
    "business",
    "entertainment",
    "general",
    "health",
    "science",
    "sports",
    "technology",
]

AVAILABLE_COUNTRY: list[str] = [
    "ae",
    "ar",
    "at",
    "au",
    "be",
    "bg",
    "br",
    "ca",
    "ch",
    "cn",
    "co",
    "cu",
    "cz",
    "de",
    "eg",
    "fr",
    "gb",
    "gr",
    "hk",
    "hu",
    "id",
    "ie",
    "il",
    "in",
    "it",
    "jp",
    "kr",
    "lt",
    "lv",
    "ma",
    "mx",
    "my",
    "ng",
    "nl",
    "no",
    "nz",
    "ph",
    "pl",
    "pt",
    "ro",
    "rs",
    "ru",
    "sa",
    "se",
    "sg",
    "si",
    "sk",
    "th",
    "tr",
    "tw",
    "ua",
    "us",
    "ve",
    "za",
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


class SearchHeadlines(Search):
    category: str | None = None
    country: str | None = None

    def model_post_init(self, __context: Any) -> None:
        if self.sources is not None and self.country is not None:
            raise ValueError("sources and country cannot be used together")
        return super().model_post_init(__context)

    @field_validator("category")
    def category_available_value(cls, value: str):
        if value not in AVAILABLE_CATEGORY:
            raise ValueError(f"category must be one of {', '.join(AVAILABLE_CATEGORY)}")
        return value

    @field_validator("country")
    def country_available_value(cls, value: str):
        if value not in AVAILABLE_COUNTRY:
            raise ValueError(f"country must be one of {', '.join(AVAILABLE_COUNTRY)}")
        return value

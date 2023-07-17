from datetime import datetime, timezone
from typing import Any

import pytest
from core.models.article import Article, NewsResponse, Source
from conftest import article_dict
from core.models.search import SearchEverything, SearchHeadlines


class TestArticle:
    def test_source_init(self) -> None:
        source: Source = Source(id="fake_id", name="fake_name")
        assert source.id == "fake_id"
        assert source.name == "fake_name"

    def test_article_init(self) -> None:
        article: Article = Article(**article_dict)
        assert article.source.id == "fake_id"
        assert article.source.name == "fake_name"
        assert article.author == "fake_author"
        assert article.title == "fake_title"
        assert article.description == "fake_description"
        assert article.url == "fake_url"
        assert article.url_to_image == "fake_url_to_image"
        assert article.published_at == datetime(
            2023, 6, 9, 17, 28, 51, tzinfo=timezone.utc
        )
        assert article.content == "fake_content"

    def test_news_init(self) -> None:
        data: dict[str, Any] = {
            "status": "fake_status",
            "totalResults": 1,
            "articles": [article_dict],
        }
        news: NewsResponse = NewsResponse(**data)
        assert news.status == "fake_status"
        assert news.total_results == 1
        assert len(news.articles) == 1


class TestSearchEverything:
    @pytest.mark.parametrize(
        "given, throwable",
        [
            (dict(q="fake_query", search_in="hello"), ValueError),
            (dict(q="fake_query", search_in="title"), None),
            (dict(q="fake_query", sort_by="hello"), ValueError),
            (dict(q="fake_query", sort_by="relevancy"), None),
            (dict(q="fake_query", language="hello"), ValueError),
            (dict(q="fake_query", language="en"), None),
        ],
    )
    def test_search_everything_validator(
        self, given: dict[str, str], throwable: Exception | None
    ) -> None:
        if throwable:
            with pytest.raises(throwable):
                SearchEverything(**given)
        else:
            search: SearchEverything = SearchEverything(**given)
            assert search.model_dump(exclude_none=True) == given


class TestSearchHeadlines:
    @pytest.mark.parametrize(
        "given, throwable",
        [
            (dict(q="fake_query", category="hello"), ValueError),
            (dict(q="fake_query", category="business"), None),
            (dict(q="fake_query", country="hello"), ValueError),
            (dict(q="fake_query", country="us"), None),
            (dict(q="fake_query", country="us", sources="bfm"), ValueError),
        ],
    )
    def test_search_headlines_validator(
        self,
        given: dict[str, str],
        throwable: Exception | None,
    ) -> None:
        if throwable:
            with pytest.raises(throwable):
                SearchHeadlines(**given)
        else:
            search: SearchHeadlines = SearchHeadlines(**given)
            assert search.model_dump(exclude_none=True) == given

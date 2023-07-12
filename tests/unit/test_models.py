from datetime import datetime, timezone

import pytest
from core.models.article import Article, Source
from conftest import article_dict
from core.models.search import SearchEverything


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


class TestSearchEverything:
    @pytest.mark.parametrize(
        "given, throwable",
        [
            (dict(q="fake_query", search_in="hello"), ValueError),
            (dict(q="fake_query", search_in="title"), None),
            (dict(q="fake_query", sort_by="hello"), ValueError),
            (dict(q="fake_query", sort_by="relevancy"), None),
        ],
    )
    def test_search_everything_test_validator(
        self, given: dict[str, str], throwable: Exception | None
    ) -> None:
        if throwable:
            with pytest.raises(throwable):
                SearchEverything(**given)
        else:
            search: SearchEverything = SearchEverything(**given)
            assert search.model_dump(exclude_none=True) == given

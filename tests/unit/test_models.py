from datetime import datetime, timezone
from core.models.article import Article, Source
from conftest import article_dict


class TestModels:
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

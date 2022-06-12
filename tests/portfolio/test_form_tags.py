from webapp.portfolio.templatetags import form_tags


def test_encode_query_dict() -> None:
    assert form_tags.encode_query_dict({"q": "testing"}) == "q=testing"

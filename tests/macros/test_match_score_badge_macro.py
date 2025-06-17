import pytest
from flask import Flask
from jinja2 import Environment, FileSystemLoader, select_autoescape


@pytest.fixture
def jinja_env():
    app = Flask(__name__)
    env = Environment(
        loader=FileSystemLoader("flasky/templates"),
        autoescape=select_autoescape(["html", "jinja2"]),
    )
    with app.app_context():
        yield env


@pytest.fixture
def match_score_badge(jinja_env):
    template = jinja_env.get_template("macros/match_score_badge.html")
    return template.module.match_score_badge


def test_render_exact_score(match_score_badge):
    html = match_score_badge(50, 60, "custom-class")
    assert "<span" in html
    assert "50" in html
    assert "60" in html
    assert "custom-class" in html
    assert "badge" in html


def test_render_score_with_one_zero(match_score_badge):
    html = match_score_badge(2, 2, "")
    default_zero_count = html.count("0")

    html = match_score_badge(0, 1)
    assert html.count("0") == default_zero_count + 1


def test_render_score_with_two_zeros(match_score_badge):
    html = match_score_badge(2, 2, "")
    default_zero_count = html.count("0")

    html = match_score_badge(0, 0)
    assert html.count("0") == default_zero_count + 2


def test_render_none_score(match_score_badge):
    html = match_score_badge(None, None, "")
    assert html.count("?") == 2

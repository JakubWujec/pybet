from flasky.standings.views import paginate

def test_paginate_multiple_pages():
    result = paginate(page=2, per_page=10, total_count=35)

    assert result["has_next"] is True
    assert result["has_prev"] is True
    assert result["next_page"] == 3
    assert result["prev_page"] == 1
    assert result["total_pages"] == 4


def test_paginate_first_page():
    result = paginate(page=1, per_page=10, total_count=35)

    assert result["has_next"] is True
    assert result["has_prev"] is False
    assert result["next_page"] == 2
    assert result["prev_page"] is None
    assert result["total_pages"] == 4


def test_paginate_last_page():
    result = paginate(page=4, per_page=10, total_count=35)

    assert result["has_next"] is False
    assert result["has_prev"] is True
    assert result["next_page"] is None
    assert result["prev_page"] == 3
    assert result["total_pages"] == 4


def test_paginate_single_page():
    result = paginate(page=1, per_page=50, total_count=35)

    assert result["has_next"] is False
    assert result["has_prev"] is False
    assert result["next_page"] is None
    assert result["prev_page"] is None
    assert result["total_pages"] == 1
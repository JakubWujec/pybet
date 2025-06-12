from flasky.generic.pagination import Pagination


def test_Pagination_multiple_pages():
    pagination = Pagination(page=2, per_page=10, total=35)

    assert pagination.has_next is True
    assert pagination.has_prev is True
    assert pagination.next_page == 3
    assert pagination.prev_page == 1
    assert pagination.total_pages == 4


def test_Pagination_first_page():
    pagination = Pagination(page=1, per_page=10, total=35)

    assert pagination.has_next is True
    assert pagination.has_prev is False
    assert pagination.next_page == 2
    assert pagination.prev_page is None
    assert pagination.total_pages == 4


def test_Pagination_last_page():
    pagination = Pagination(page=4, per_page=10, total=35)

    assert pagination.has_next is False
    assert pagination.has_prev is True
    assert pagination.next_page is None
    assert pagination.prev_page == 3
    assert pagination.total_pages == 4


def test_Pagination_single_page():
    pagination = Pagination(page=1, per_page=50, total=35)

    assert pagination.has_next is False
    assert pagination.has_prev is False
    assert pagination.next_page is None
    assert pagination.prev_page is None
    assert pagination.total_pages == 1

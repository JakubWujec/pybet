from dataclasses import dataclass


@dataclass
class Pagination:
    page: int
    per_page: int
    total: int

    @property
    def total_pages(self):
        return (self.total + self.per_page - 1) // self.per_page

    @property
    def has_next(self):
        return self.page < self.total_pages

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def next_page(self):
        return self.page + 1 if self.has_next else None

    @property
    def prev_page(self):
        return self.page - 1 if self.has_prev else None

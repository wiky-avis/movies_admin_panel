from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from api.v1.mixins import MoviesApiMixin


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            self.get_queryset(), self.paginate_by
        )
        return {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "page": page.number,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": list(queryset),
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, object, **kwargs):
        return object

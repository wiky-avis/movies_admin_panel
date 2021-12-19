from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse

from movies.models import FilmWork, PersonRole


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def _aggregate_person(role: str):
        return ArrayAgg(
            "filmworkperson__person_id__full_name",
            filter=Q(filmworkperson__role=role),
            distinct=True,
        )

    @classmethod
    def get_queryset(cls):
        return FilmWork.objects.select_related('film_persons', 'film_genres').annotate(
            genres=ArrayAgg("film_genres__name", distinct=True),
            actors=cls._aggregate_person(role=PersonRole.ACTOR),
            directors=cls._aggregate_person(role=PersonRole.DIRECTOR),
            writers=cls._aggregate_person(role=PersonRole.WRITER),
        ).values()

    @staticmethod
    def render_to_response(context, **response_kwargs):
        return JsonResponse(context)

import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.fields import AutoCreatedField, AutoLastModifiedField


class MixinTimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = AutoCreatedField(_('created_at'))
    updated_at = AutoLastModifiedField(_('updated_at'))

    class Meta:
        abstract = True


class Genre(MixinTimeStampedModel):
    name = models.CharField(_('название'), max_length=255)
    description = models.TextField(_('описание'), blank=True)

    class Meta:
        verbose_name = _('жанр')
        verbose_name_plural = _('жанры')
        db_table = "genre"

    def __str__(self):
        return self.name


class FilmWorkType(models.TextChoices):
    MOVIE = 'movie', _('фильм')
    TV_SHOW = 'tv_show', _('шоу')


class FilmWork(MixinTimeStampedModel):
    title = models.CharField(_('название'), max_length=255)
    description = models.TextField(_('описание'), blank=True)
    creation_date = models.DateField(_('дата создания фильма'), blank=True)
    certificate = models.TextField(_('сертификат'), blank=True)
    file_path = models.FileField(_('файл'), upload_to='film_works/', blank=True)
    rating = models.FloatField(_('рейтинг'), validators=[MinValueValidator(0)], blank=True)
    type = models.CharField(_('тип'), max_length=20, choices=FilmWorkType.choices)
    genres = models.ManyToManyField(Genre, through='FilmWorkGenre')

    class Meta:
        verbose_name = _('кинопроизведение')
        verbose_name_plural = _('кинопроизведения')
        db_table = "film_work"

    def __str__(self):
        return self.title


class FilmWorkGenre(MixinTimeStampedModel):
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE, to_field='id', db_column='film_work_id')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, to_field='id', db_column='genre_id')

    class Meta:
        indexes = [
            models.Index(fields=['film_work_id', 'genre_id'], name='film_work_genre'),
        ]
        verbose_name = _('Жанр фильма')
        verbose_name_plural = _('Жанры фильмов')
        db_table = "genre_film_work"

    def __str__(self):
        return str(f'{self.film_work} - {self.genre}')


class PersonRole(models.TextChoices):
    ACTOR = 'actor', _('актер')
    DIRECTOR = 'director', _('режисер')
    WRITER = 'writer', _('писатель')


class Person(MixinTimeStampedModel):
    full_name = models.CharField(_('имя'), max_length=255)
    birth_date = models.DateField(_('дата рождения'))

    class Meta:
        verbose_name = _('Персона')
        verbose_name_plural = _('Персоны')
        db_table = "person"

    def __str__(self):
        return self.full_name


class PersonFilmWork(MixinTimeStampedModel):
    film_work = models.ForeignKey(
        FilmWork, on_delete=models.CASCADE, to_field='id', db_column='film_work_id'
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, to_field='id', db_column='person_id'
    )
    role = models.CharField(_('профессия'), max_length=20, choices=PersonRole.choices)

    class Meta:
        db_table = "person_film_work"
        indexes = [
            models.Index(fields=['film_work_id', 'person_id', 'role'], name='film_work_person'),
        ]

    def __str__(self):
        return str(f'{self.film_work} - {self.person}')

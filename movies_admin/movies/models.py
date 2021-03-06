import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.fields import AutoCreatedField, AutoLastModifiedField


class UpdatedCreatedMixin(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = AutoCreatedField(_('created_at'))
    updated_at = AutoLastModifiedField(_('updated_at'))

    class Meta:
        abstract = True


class Genre(UpdatedCreatedMixin, models.Model):
    name = models.CharField(_('название'), max_length=255)
    description = models.TextField(_('описание'), blank=True)

    class Meta:
        verbose_name = _('жанр')
        verbose_name_plural = _('жанры')
        db_table = '"content"."genre"'
        ordering = ('name',)
        managed = False

    def __str__(self):
        return self.name


class FilmWorkType(models.TextChoices):
    MOVIE = 'movie', _('фильм')
    TV_SHOW = 'tv_show', _('шоу')


class FilmWork(UpdatedCreatedMixin, models.Model):
    title = models.CharField(_('название'), max_length=255)
    description = models.TextField(_('описание'), blank=True)
    creation_date = models.DateField(_('дата создания фильма'), blank=True)
    certificate = models.TextField(_('сертификат'), blank=True)
    file_path = models.FileField(_('файл'), upload_to='film_works/', blank=True)
    rating = models.FloatField(_('рейтинг'), validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True)
    type = models.CharField(_('тип'), max_length=20, choices=FilmWorkType.choices)
    film_genres = models.ManyToManyField(Genre, through='FilmWorkGenre')
    film_persons = models.ManyToManyField('Person', through='FilmWorkPerson')

    class Meta:
        verbose_name = _('кинопроизведение')
        verbose_name_plural = _('кинопроизведения')
        db_table = '"content"."film_work"'
        ordering = ('title', )
        managed = False

    def __str__(self):
        return self.title


class FilmWorkGenre(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE, to_field='id', db_column='film_work_id')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, to_field='id', db_column='genre_id')
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['film_work_id', 'genre_id'], name='film_work_genre'),
        ]
        verbose_name = _('Жанр фильма')
        verbose_name_plural = _('Жанры фильмов')
        ordering = ('id',)
        db_table = '"content"."genre_film_work"'

    def __str__(self):
        return str(f'{self.film_work} - {self.genre}')


class PersonRole(models.TextChoices):
    ACTOR = 'actor', _('актер')
    DIRECTOR = 'director', _('режисер')
    WRITER = 'writer', _('писатель')


class Person(UpdatedCreatedMixin, models.Model):
    full_name = models.CharField(_('имя'), max_length=255)
    birth_date = models.DateField(_('дата рождения'))

    class Meta:
        verbose_name = _('Персона')
        verbose_name_plural = _('Персоны')
        db_table = '"content"."person"'
        ordering = ('full_name',)
        managed = False

    def __str__(self):
        return self.full_name


class FilmWorkPerson(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    film_work = models.ForeignKey(
        FilmWork, on_delete=models.CASCADE, to_field='id', db_column='film_work_id'
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, to_field='id', db_column='person_id'
    )
    role = models.CharField(_('профессия'), max_length=20, choices=PersonRole.choices)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"content"."person_film_work"'
        indexes = [
            models.Index(fields=['film_work_id', 'person_id', 'role'], name='film_work_person'),
        ]
        ordering = ('id',)

    def __str__(self):
        return str(f'{self.film_work} - {self.person}')

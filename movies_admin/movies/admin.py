from django.contrib import admin

from .models import FilmWork, FilmWorkGenre, FilmWorkPerson, Genre, Person


class PersonRoleInline(admin.TabularInline):
    model = FilmWorkPerson
    extra = 0


class GenreInline(admin.TabularInline):
    model = FilmWorkGenre
    extra = 0


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'creation_date', 'rating')
    list_filter = ('type', )
    search_fields = ('title', 'description', 'id')
    fields = ('certificate', 'title', 'type', 'description', 'creation_date', 'file_path', 'rating')
    inlines = [
        PersonRoleInline,
        GenreInline
    ]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass

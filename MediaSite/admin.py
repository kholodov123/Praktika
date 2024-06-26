from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin 

from .models import Actor, Category, Movie, Genre, Reviews, Rating, MovieShots, LikeDislike, Ticket, Shift, Status, Cart


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 0
    readonly_fields = ('name', 'movie', 'parent')


class MovieShortsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110">')

    get_image.short_description = 'Фото'


@admin.register(Movie)
class MovieAdmin(TabbedTranslationAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'country', 'kinopoisk_rating', 'year', 'slug')
    list_filter = ('category', 'kinopoisk_rating', 'year', 'genres', 'country')
    search_fields = ('title', 'category__name')
    readonly_fields = ('get_poster',)
    save_on_top = True
    inlines = [MovieShortsInline, ReviewInline]
    fields = (
        ('title', 'tagline', 'kinopoisk_id'), ('description'), ('poster', 'get_poster'),
        ('year', 'world_premiere', 'country'),
        ('directors', 'actors', 'genres',),
        ('budget', 'fess_in_world',), ('kinopoisk_rating',), ('category', 'running_time'),
        ('slug', 'draft')
    )

    def get_poster(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="60">')

    get_poster.short_description = 'Постер'


@admin.register(Actor)
class ActorAdmin(TranslationAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'age')
    readonly_fields = ('get_image',)
    list_display_links = ('name', 'slug', 'age')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = 'Фото'


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug',)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('movie', 'name', 'ip', 'parent', 'rating')
    list_filter = ('parent', 'created_at', 'movie', 'rating')
    readonly_fields = ('movie', 'name', 'rating', 'parent')


@admin.register(MovieShots)
class MovieShorts(TranslationAdmin):
    list_display = ('title', 'movie', 'get_image')
    list_filter = ('title', 'movie')
    search_fields = ('movie', 'title')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = 'Фото'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'avg_rating')
    readonly_fields = ('movie', 'avg_rating', 'count_reviews', 'sum_rating')


@admin.register(LikeDislike)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user_ip', 'content_object', 'object_id')

admin.site.register([Status, Cart])   

@admin.register(Ticket)    
class TicketAdmin(admin.ModelAdmin):
    list_display = ('number', 'movie', 'cart', 'status')

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'start_time', 'end_time')
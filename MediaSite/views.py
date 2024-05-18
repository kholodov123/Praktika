import json
import logging

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponseServerError
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import BaseCreateView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.admin.views.decorators import staff_member_required


from MediaSite.forms import ReviewForm, UserRegisterForm, UserLoginForm
from MediaSite.models import Movie, Genre, Actor, Rating, Reviews, LikeDislike, Shift, Ticket, Status, Cart


def main(request):
    return render(request, "MediaSite/main.html")

def login(request):
    return render(request, "MediaSite/login.html")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@staff_member_required
def adminpage(request):
    try:
        users = User.objects.all()
        movies = Movie.objects.all()
        shifts = Shift.objects.all()
        tickets = Ticket.objects.all()
        return render(request, "MediaSite/administrator.html", {'users':users, 'shifts':shifts, 'tickets':tickets, 'movies':movies})
    except Exception as e:
        return HttpResponseServerError(str(e))
    
@staff_member_required
def update_ticket_status(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    if request.method == 'POST':
        new_status_id = request.POST.get('new_status')
        new_status = Status.objects.get(pk=new_status_id)
        ticket.status = new_status
        ticket.save()
        return redirect('adminpage')

    statuses = Status.objects.all()
    return render(request, 'MediaSite/update_ticket_status.html', {'ticket': ticket, 'statuses': statuses})

def buy_ticket(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie')
        status_id = request.POST.get('status')
        user = request.user

        movie = Movie.objects.get(pk=movie_id)
        status = Status.objects.get(pk=status_id)

        cart, created = Cart.objects.get_or_create(user=user)

        ticket = Ticket(movie=movie, cart=cart, status=status)
        ticket.save()

        cart.tickets.add(ticket)
        cart.save()

        return redirect('home')

    movies = Movie.objects.all()
    statuses = Status.objects.all()
    return render(request, 'MediaSite/buy_ticket.html', {'movies': movies, 'statuses': statuses})

def view_cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    tickets = cart.tickets.all()

    return render(request, 'MediaSite/cart.html', {'tickets': tickets})

def superuser_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return wrap
    
class MoviesFilter:

    def get_genres(self):
        return Genre.objects.all().order_by('name')

    def get_years(self):
        return Movie.objects.values_list('year', flat=True).distinct().order_by('-year')

    def get_countries(self):
        return Movie.objects.values_list('country', flat=True).distinct().order_by('country')


class MoviesView(MoviesFilter, View):
    model = Movie
    template_name = 'MediaSite/main.html'

    def get(self, request):
        carousel_movies = Movie.objects.order_by('kinopoisk_rating')[:12].prefetch_related('genres')
        premieres = Movie.objects.order_by('-world_premiere')[:8].prefetch_related('genres').select_related('category')
        new_movies = Movie.objects.order_by('-year')[:18].prefetch_related('genres')
        try:
            cartoon_id = Genre.objects.get(slug='multfilm')
        except Genre.DoesNotExist:
            cartoon_id = None
        cartoons_list = Movie.objects.filter(genres=cartoon_id).order_by('-year')[:12].prefetch_related('genres')

        context = {'carousel_list': carousel_movies, 'premieres_list': premieres, 'cartoons_list': cartoons_list,
                   'new_movies_list': new_movies}
        return render(request, 'MediaSite/main.html', context)


class SingleMovieView(MoviesFilter, DetailView, BaseCreateView):
    model = Movie
    template_name = 'MediaSite/mediaview.html'
    context_object_name = 'movie'
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Reviews.objects.filter(movie=kwargs['object'].id, parent__isnull=True).all()
        context['review_children'] = Reviews.objects.filter(movie=kwargs['object'].id, parent__isnull=False).all()
        context['recommended_films'] = Movie.objects.filter(
            genres__in=(kwargs['object'].genres.all().values_list('pk').distinct()))[:6]
        return context


class AddReview(View):

    def rating_for_movie(self, pk, rating):

        try:
            rating_obj = Rating.objects.get(movie_id=pk)
            count_r = int(rating_obj.count_reviews) + 1
            sum_r = int(rating_obj.sum_rating) + rating
            avg_r = round(sum_r / count_r, 1)

            rating_obj.count_reviews = count_r
            rating_obj.sum_rating = sum_r
            rating_obj.avg_rating = avg_r
            rating_obj.save()

        except ObjectDoesNotExist:

            Rating.objects.create(count_reviews=1,
                                  sum_rating=rating,
                                  avg_rating=rating,
                                  movie_id=pk)

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)

        if form.is_valid():
            form = form.save(commit=False)

            if form.rating:
                ip = get_client_ip(self.request)
                user_old_rating = Reviews.objects.filter(movie=pk, ip=ip)
                if user_old_rating:
                    form.rating = 0
                else:
                    form.rating = 2 * form.rating
                    self.rating_for_movie(pk, int(form.rating))
                form.ip = ip

            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorDetailView(DetailView, MultipleObjectMixin):
    model = Actor
    template_name = 'MediaSite/actor_detail.html'
    context_object_name = 'actor'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        object_list = Movie.objects.filter(actors=self.object).prefetch_related('genres')
        context = super().get_context_data(object_list=object_list, **kwargs)

        return context


class DirectorDetailView(DetailView, MultipleObjectMixin):
    model = Actor
    template_name = 'MediaSite/directors_detail.html'
    context_object_name = 'director'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        object_list = Movie.objects.filter(directors=self.object).prefetch_related('genres')
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context




class CatalogView(MoviesFilter, ListView):
    model = Movie
    template_name = 'MediaSite/catalog_movies.html'
    context_object_name = 'movies'
    paginate_by = 12

    def get_queryset(self):
        
        if self.kwargs.get('slug'):
            genres = Genre.objects.get(slug=self.kwargs['slug'])
            queryset = Movie.objects.filter(genres=genres.id).prefetch_related('genres')
        else:
            queryset = Movie.objects.order_by('year').prefetch_related('genres')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('slug'):
            context['current_genre'] = self.kwargs['slug']

        return context


class FilterMoviesView(MoviesFilter, ListView):
    template_name = 'MediaSite/catalog_movies.html'
    paginate_by = 12
    context_object_name = 'movies'

    def result_queryset(self, genres, year, country):
        if year and genres and country:
            queryset = Movie.objects.filter(genres=genres, year=year, country=country).prefetch_related('genres')
        elif year is None and (genres and country):
            queryset = Movie.objects.filter(genres=genres, country=country).distinct().prefetch_related('genres')
        elif genres is None and (year and country):
            queryset = Movie.objects.filter(year=year, country=country).distinct().prefetch_related('genres')
        elif country is None and (year and genres):
            queryset = Movie.objects.filter(year=year, genres=genres).distinct().prefetch_related('genres')
        else:
            queryset = Movie.objects.filter(
                Q(genres=genres) | Q(country=country) | Q(year=year)).distinct().prefetch_related('genres')

        return queryset

    def get_queryset(self):
        genres = None
        if self.request.GET.get('genre') not in ['Genre', 'Жанр']:
            genres = Genre.objects.get(name=self.request.GET.get('genre')).id

        country = None if self.request.GET.get('country') in ['Country', 'Страна'] else self.request.GET.get('country')
        year = None if self.request.GET.get('year') in ['Year', 'Год'] else self.request.GET.get('year')
        queryset = self.result_queryset(genres, year, country).order_by('year')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["url_genre"] = f'genre={self.request.GET.get("genre")}&'
        context["country"] = f"year={self.request.GET.get('year')}&"
        context["year"] = f"country={self.request.GET.get('country')}&"
        return context

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'MediaSite/registration.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()

        if form.cleaned_data.get('is_staff'):
            user.is_staff = True

        if form.cleaned_data.get('is_superuser'):
            user.is_superuser = True

        user.save()

        login(self.request, user)
        return redirect('/')


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'MediaSite/login.html'
    next_page = '/'


def logout_user(request):
    logout(request)
    return redirect('login')


def handle_not_found(request, exception):
    return render(request, '404.html')


class Search(ListView):
    template_name = 'MediaSite/catalog_movies.html'
    context_object_name = 'movies'
    paginate_by = 12

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q').title())

    def get_context_data(self, *args, **kwargs):
        context = super(Search, self).get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context


def about_us(request):
    return render(request, 'MediaSite/about.html')


def faq_page(request):
    return render(request, 'MediaSite/help_page.html')

def terms_page(request):
    return render(request, 'MediaSite/terms_of_use.html')

class VotesView(View):
    model = Reviews  # Модель данных - Статьи или Комментарии
    vote_type = None  # Тип комментария Like/Dislike

    def post(self, request, pk, slug):
        obj = self.model.objects.get(pk=pk)
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(
                obj), object_id=obj.id, user_ip=get_client_ip(request))
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:

            obj.votes.create(user_ip=get_client_ip(request), vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )

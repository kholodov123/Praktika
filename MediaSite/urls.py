
from django.urls import path
from django.views.decorators.cache import cache_page
from MediaSite import views


from .views import *

DEBUG = True

if DEBUG == True:
    urlpatterns = [
        path('home/', (MoviesView.as_view()), name='home'),
        path('catalog/<int:page>/', (CatalogView.as_view()), name='catalog'),
        path('filter/', (FilterMoviesView.as_view()), name='filter'),
        path('search/', (Search.as_view()), name='search'),
        path('about/', (about_us), name='about'),
        path('help/', (faq_page), name='help_page'),
        path('termsofuse/', (terms_page), name='terms_of_use'),
        path('register/', (UserRegisterView.as_view()), name='register'),
        path('login/', UserLoginView.as_view(), name='login'),
        path('logout/', logout_user, name='logout'),
        path('adminpage/', adminpage, name='adminpage'),
        path('update_ticket_status/<int:ticket_id>/', views.update_ticket_status, name='update_ticket_status'),
        path('buy_ticket/', views.buy_ticket, name='buy_ticket'),
        path('view_cart/', views.view_cart, name='view_cart'),
        path('catalog/<slug:slug>/<int:page>/', (CatalogView.as_view()), name='genre_catalog'),
        path('<slug:slug>/', SingleMovieView.as_view(), name='movie_detail'),
        path("actor/<str:slug>/<int:page>/", (ActorDetailView.as_view()), name="actor_detail"),
        path("producer/<str:slug>/<int:page>/", (DirectorDetailView.as_view()), name="director_detail"),
    ]
else:
    urlpatterns = [
        path('home/', cache_page(60 * 10)(MoviesView.as_view()), name='home'),
        path('catalog/<int:page>/', cache_page(60 * 10)(CatalogView.as_view()), name='catalog'),
        path('filter/', cache_page(60 * 10)(FilterMoviesView.as_view()), name='filter'),
        path('search/', cache_page(60 * 10)(Search.as_view()), name='search'),
        path('about/', cache_page(60 * 10)(about_us), name='about'),
        path('help/', cache_page(60 * 10)(faq_page), name='help_page'),
        path('termsofuse/', cache_page(60 * 10)(terms_page), name='terms_of_use'),
        path('register/', cache_page(60 * 10)(UserRegisterView.as_view()), name='register'),
        path('login/', UserLoginView.as_view(), name='login'),
        path('logout/', logout_user, name='logout'),
        path('adminpage/', adminpage, name='adminpage'),
        path('update_ticket_status/<int:ticket_id>/', views.update_ticket_status, name='update_ticket_status'),
        path('buy_ticket/', views.buy_ticket, name='buy_ticket'),
        path('view_cart/', views.view_cart, name='view_cart'),
        path('catalog/<slug:slug>/<int:page>/', cache_page(60 * 10)(CatalogView.as_view()), name='genre_catalog'),
        path('<slug:slug>/', SingleMovieView.as_view(), name='movie_detail'),
        path("actor/<str:slug>/<int:page>/", cache_page(60 * 10)(ActorDetailView.as_view()), name="actor_detail"),
        path("producer/<str:slug>/<int:page>/", cache_page(60 * 10)(DirectorDetailView.as_view()), name="director_detail"),
    ]
"""ratingmovieapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from movie import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register',views.RegistrationView.as_view(),name="register"),
    path("login",views.SignInView.as_view(),name="signin"),


    path("home",views.IndexView.as_view(),name="home"),
    path("logout",views.SignOutView.as_view(),name="signout"),


    path("profile/add",views.ProfileCreateView.as_view(),name="profile-add"),
    path("",views.HomePageView.as_view(),name="homepage"),
    path("profile",views.MyProfileView.as_view(),name="myprofile"),
    path("profile/change/<int:pk>",views.ProfileEditView.as_view(),name="profile-edit"),

    path("movie/add",views.MovieCreateView.as_view(),name="movie-add"),
    path("movie/all",views.MovieListView.as_view(),name="movie-list"),
    path("movie/<int:pk>",views.MovieDetailView.as_view(),name="movie-detail"),
    path("movie/remove/<int:pk>",views.MovieDeleteView.as_view(),name="movie-delete"),
    path("movie/change/<int:pk>",views.MovieEditView.as_view(),name="movie-edit"),


    
    path("movies/all",views.MovieListaView.as_view(),name="movie-lista"),


    
 
    
  
    path("movies/shop",views.ShopView.as_view(),name="shopmovie"),


    
    path('movie/<int:movie_id>/add-to-wishlist/',views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/',views.wishlist, name='wishlist'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



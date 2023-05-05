
from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import View,CreateView,TemplateView,ListView,DetailView,DeleteView,UpdateView,FormView

from django.contrib.auth.models import User
from movie.forms import RegistrationForm,LoginForm,UserProfileForm,MovieForm,RatingMovieForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from movie.models import Movies,RatingMovie,UserProfile,Wishlist
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django_filters import FilterSet
from django.views.decorators.cache import never_cache


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_required,never_cache]




class RegistrationView(SuccessMessageMixin,CreateView):
    model=User
    template_name="register.html"
    form_class=RegistrationForm 
    success_url=reverse_lazy("signin")
    success_message="registration completed succesfully"

class SignInView(FormView):
    form_class=LoginForm
    template_name="login.html"
    def post(self,request,*args,**kwargs):
    
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            
            if usr:
                login(request,usr)
                return redirect("home")
               
            else:
                messages.error(request,"given credentials are not valid !")
                return render(request,self.template_name,{"form":form})
            

class HomePageView(TemplateView):
    template_name="index.html"


class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        messages.success(request,"logout successfully")
        return redirect("signin")
    

class IndexView(CreateView,ListView):
    model=Movies
    form_class=MovieForm
    template_name="base.html"
    success_url=reverse_lazy("home")
    context_object_name="movies"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
    def get_queryset(self):
        return Movies.objects.all().order_by("-created_date")
    
    



class ProfileCreateView(CreateView):
    form_class=UserProfileForm
    template_name="profile-add.html"
    success_url=reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
class MyProfileView(TemplateView):
    template_name="profile.html"



class ProfileEditView(UpdateView):
    model=UserProfile
    form_class=UserProfileForm
    template_name="profile-edit.html"
    success_url=reverse_lazy("myprofile")

class MovieCreateView(CreateView):
    model=Movies
    form_class=MovieForm
    template_name="movie-add.html"
    success_url=reverse_lazy("movie-list")


class MovieFilter(FilterSet):
    class Meta:
        model=Movies
        fields=["language","director","runningtime","year","genre","title"]

class MovieListView(ListView):
    model=Movies
    context_object_name="movies"
    template_name="movie-list.html"
    def get(self,request,*args,**kwargs):
        f=MovieFilter(request.GET,queryset=Movies.objects.all())
        return render (request,self.template_name,{"filter":f})
    

from django.shortcuts import get_object_or_404
class MovieDetailView(DetailView):
    model=Movies
    
    template_name="movie-detail.html"
    context_object_name="movie"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rating_form"] = RatingMovieForm(initial={'movie': self.object, 'user': self.request.user})
        context["ratings"] = RatingMovie.objects.filter(movie=self.object)
        return context

    def post(self, request, *args, **kwargs):
        movie = self.get_object()
        rating_form = RatingMovieForm(request.POST)
        if rating_form.is_valid():
            rating_form.save()
            return redirect('movie-detail', pk=movie.pk)
        context = self.get_context_data()
        context['rating_form'] = rating_form
        return self.render_to_response(context)




  

class MovieDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Movies.objects.get(id=id).delete()
        return redirect("movie-list")
    

class MovieEditView(UpdateView):
    model=Movies
    form_class=MovieForm
    template_name="movie-edit.html"
    success_url=reverse_lazy("movie-list")


class MovieFilter(FilterSet):
    class Meta:
        model=Movies
        fields=["language","director","runningtime","year","genre","title"]

class MovieListaView(ListView):
    model=Movies
    context_object_name="movies"
    template_name="movie-all.html"
    def get(self,request,*args,**kwargs):
        k=MovieFilter(request.GET,queryset=Movies.objects.all())
        return render (request,self.template_name,{"filter":k})
    



class ShopView(TemplateView):
    template_name="shop.html"
    


def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist': wishlist}
    return render(request, 'wishlist.html', context)


    



    




def add_to_wishlist(request, movie_id):
    movie = get_object_or_404(Movies, id=movie_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user,movie=movie)
    wishlist.movie.save()
    if created:
        messages.success(request, f"{movie.title} has been added to your wishlist!")
    else:
        messages.warning(request, f"{movie.title} is already in your wishlist!")
    return redirect('movie-detail', pk=movie_id)
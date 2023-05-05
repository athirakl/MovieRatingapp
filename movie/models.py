from django.db import models

# Create your models here.
from django.contrib.auth.models import User







class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return self.user.username
    


class Movies(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    language=models.CharField(max_length=200)
    director=models.CharField(max_length=200)
    description = models.TextField()
    runningtime=models.FloatField()
    year=models.IntegerField()
    genre=models.CharField(max_length=200)
    poster=models.ImageField(upload_to="images",null=True,blank=True)
   
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class RatingMovie(models.Model):
    RATING_CHOICES = (
        (1, '1 stars'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    )
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, related_name='rating_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)




    def __str__(self):
        return self.movie
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)



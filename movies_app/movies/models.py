from django.db import models
from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator


class Movie(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    image = models.CharField(max_length=200)
    details = models.CharField(max_length=500)
    genre = models.CharField(max_length=50)
    duration = models.CharField(max_length=20)
    classification = models.CharField(max_length=50)
    avg_rating = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )

    def __str__(self):
        return self.title


class Rating(models.Model):

    number = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    comment = models.CharField(max_length=200, default='')
    movie = models.ForeignKey(Movie, default=1, on_delete=models.CASCADE)

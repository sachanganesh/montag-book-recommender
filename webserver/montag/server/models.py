from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator, EmailValidator

class Book(models.Model):
	isbn = 	    models.CharField(max_length=13)
	title =     models.CharField(max_length=100)
	author =    models.CharField(max_length=100)
	pub_year =  models.SmallIntegerField()
	publisher = models.CharField(max_length=100)
	img_s =     models.URLField(
					max_length=350,
					validators=[URLValidator]
				)
	img_m =     models.URLField(
					max_length=350,
					validators=[URLValidator]
				)
	img_l =     models.URLField(
					max_length=350,
					validators=[URLValidator]
				)


class Rating(models.Model):
	user =      models.ForeignKey(User, on_delete=models.DO_NOTHING)
	book =      models.ForeignKey(Book, on_delete=models.DO_NOTHING)
	rating =    models.SmallIntegerField(
					validators=[MinValueValidator(0), MaxValueValidator(10)]
				)

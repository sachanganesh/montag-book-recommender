from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator, EmailValidator

class Book(models.Model):
	isbn = 	    models.CharField(max_length=13)
	title =     models.CharField(max_length=350)
	author =    models.CharField(max_length=350)
	pub_year =  models.SmallIntegerField()
	publisher = models.CharField(max_length=350)
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
	user =      models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False)
	book =      models.ForeignKey(Book, on_delete=models.DO_NOTHING)
	rating =    models.SmallIntegerField(
					validators=[MinValueValidator(0), MaxValueValidator(10)]
				)

class Recommender(models.Model):
	version =   models.AutoField(primary_key=True)
	model =     models.BinaryField()

	class Meta:
		ordering = ('-version',)

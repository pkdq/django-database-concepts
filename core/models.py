from django.db import models

# Create your models here.
class Simple(models.Model):
	text = models.CharField(max_length=100)
	number = models.IntegerField(null=True)
	url = models.URLField(default='www.abc.com')


	def __str__(self):
		return self.text

class Language(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Framework(models.Model):
	name = models.CharField(max_length=100)
	language = models.ForeignKey(Language, on_delete=models.CASCADE)

	def __str__(self):
		return self.name


class Movie(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Actor(models.Model):
	name = models.CharField(max_length=100)
	movies = models.ManyToManyField(Movie, related_name='actors')

	def __str__(self):
		return self.name


class Character(models.Model):
	name = models.CharField(max_length=100)
	movies = models.ManyToManyField(Movie, related_name='characters')

	def __str__(self):
		return self.name


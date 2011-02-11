from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Exercise(models.Model):
	name = models.CharField(max_length = 100)
	def __unicode__(self):
		return self.name
	
class DayExercise(models.Model):
	date = models.DateTimeField(auto_now_add = True)
	count = models.IntegerField()
	name = models.ForeignKey(Exercise)
	username = models.ForeignKey(User)

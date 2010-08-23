from django.db import models

# Create your models here.

class Profile(models.Model):
	uid = models.CharField(max_length = 40)
	name = models.CharField(max_length = 300)
	email = models.EmailField(max_length = 100)
	password = models.CharField(max_length = 300)
	cookie = models.CharField(max_length = 300)
	cookie_date = models.DateTimeField('date')
	def __unicode__(self):
		return self.name

#Contact model is for vkaccounts to be parsed
class Contact(models.Model):
	uid = models.CharField(max_length = 40)
	name = models.CharField(max_length = 150)
#	profile = models.ForeignKey(Profile) #which profile will parse this vkid
	def __unicode__(self):
		return str(self.uid)

class Status(models.Model):
	contact = models.ForeignKey(Contact)
	text = models.CharField(max_length = 600)
	date = models.DateTimeField('date')
	def __unicode__(self):
		return self.text
		
		
class Comment(models.Model):
	status = models.ForeignKey(Status)
	text = models.TextField()
	date = models.DateTimeField('date')
	email = models.CharField(max_length = 50)
	def __unicode__(self):
		return self.text

#class ParseList(models.Model):
#	uid = models.CharField(max_length = 40)
#	name = models.CharField(max_length = 150)
#	isparsing = models.BooleanField()

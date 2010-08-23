#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import django libs
import os, sys
import django
from django.core.management import execute_manager
# Import our site settings
import settings
# Set DJANGO_SETTINGS_MODULE  environment variable to settings
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"
# Now we can continue
import robot
from robot import models
from robot.models import Status
from robot.models import Contact
from robot.models import Profile
from robot.models import Comment
import datetime
import urllib
import urllib2
from get_between import get_between


####### API go here
def get_cookie(email,passw,filter_):
	#function returns vk.com cookie; arguments -- email, password & news filter
	url = 'http://login.vk.com/?act=login'	

	values = {
		'expire' : '',
		'vk': '1',
		'email' : email,
		'pass' : passw
		}

	data = urllib.urlencode(values)

	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
		'Accept': 'text/html,application/xhtml+xml,application/xml',
		'Accept-Language': 'en-us,en',
		'Accept-Charset': 'ISO-8859-1,utf-8',
		'Referer': 'http://vk.com/index.php',
		'Cookie': 'remixlang=3; remixchk=5',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Content-Length': str(len(data))
		}

	Response = urllib2.urlopen(urllib2.Request(url, data, headers))
	string = Response.read()
	
	string = get_between(string,0,'\'s\'','/>')
	if string == None:
		print 'None :('
		return None

	values = 'remixlang=3; remixchk=5; remixsid=' + get_between(string,0,'value=\'','\'') + '; remixnews_privacy_filter=0; remixnews_types=' + filter_
	return values
	

def get_cookies():
	cookies = []
	for i in Profile.objects.all():
		cookies.append(get_veified_cookie(i))
	return cookies


def is_contact_in_base(new_uid):
	if Contact.objects.filter(uid = new_uid):
		return True
	return False


def is_status_in_base(status_uid,status_text,status_date):
	this_contact = Contact.objects.get(uid = status_uid)
	if Status.objects.filter(contact = this_contact.id,text = status_text,date = status_date):
		return True
	return False


#add profile to database
def add_profile(email_,password_):
	date = datetime.datetime(2001,1,1)
	try:
		Profile.objects.get(email = email_)
	except Profile.DoesNotExist:
		Profile(uid = 'one',name = 'unknown',password = password_,email = email_,cookie = 'empty',cookie_date = date).save()
		return True
	return False


#add contact to database
def add_contact(Uid,Name):
	contact = Contact(uid=Uid, name=Name)
	contact.save()
	return contact.uid

#add status to database
def add_status(Uid,Status_text,Date):
	author = Contact.objects.get(uid = Uid)
	status = Status(contact = author, text = Status_text, date = Date)
	status.save()
	return status.text
	
	
#add comment to database
def add_comment(status_id,comment_text,author_email):
	try:
		new_status = Status.objects.get(id=status_id)
	except Status.DoesNotExist:
		return None
	if not (author_email.find('@') or author_email.find('.')):
		return None
	comment = Comment(status = new_status,text = comment_text,date = datetime.datetime.now(),email = author_email)
	comment.save()
	return comment.text
	
	
def get_comments(stat):
	comments = Comment.objects.filter(status = stat).order_by('date')
	return comments	
	

#get status from database by id
def get_status(stat_id):
	try:
		status = Status.objects.get(id = stat_id)
	except Status.DoesNotExist:
		status = None
	return status


#get contact from database by id
def get_contact(cont):
	try:
		contact = Contact.objects.get(id = cont.id)
	except Contact.DoesNotExist:
		contact = None
	return contact
	

#get number of commnets by status id
def get_number_of_comments(stat_id):
	stat = get_status(stat_id)
	if stat:
		return len(Comment.objects.filter(status = stat))
	else:
		return 0
		
		
def get_veified_cookie(profile):
	now = datetime.datetime.now()
	if (now - profile.cookie_date).seconds > 300:
		filter_ = '2147292448'
		new_cookie = get_cookie(profile.email,profile.password,filter_)
		if new_cookie == None:
			print 'GetCookie Error'
			return ''
		else:
			profile.cookie = new_cookie
			profile.cookie_date = now
			profile.save()
	return profile.cookie;






####### old API go here
def getLastStatus(vkid):
	#TODO Add exception handling
	idContact = Contact.objects.get(uid = vkid)
	lastStatus = idContact.status_set.all().order_by('-date') [:1].get()
	text = lastStatus.text
	date = lastStatus.date
	return text, date

def setStatus(vkid, vktext, vkdate): #please, follow right date format
	#TODO Add exception handling
	idContact = Contact.objects.get(uid = vkid)
	idContact.status_set.create(text = vktext, date = vkdate)
	text = idContact.status_set.all().order_by('date') [:1].get().text
	return text

def listContacts(vkaccount):
	#TODO Add exception handling
	listCon = []
	idProfile = Profile.objects.get(uid = vkaccount)
	for i in idProfile.contact_set.all():
		listCon.append(i.uid)
	return listCon

def listProfiles():
	#TODO Add exception handling
	listProfiles = []
	for i in Profile.objects.all():
		listProfiles.append(i.uid)
	return listProfiles

def getProfileLoginfo(profileid):
	#TODO add exception handling
	idProfile = Profile.objects.get(id=profileid)
	mail = idProfile.email
	passw = idProfile.password
	return mail, passw	

def addContact(vkaccount, vkid, vkname, vkisparsing):
	#TODO Add exception handling
	idProfile = Profile.objects.get(uid = vkaccount)
	newContact = idProfile.contact_set.create(uid = vkid, name = vkname, isparsing = vkisparsing)
	return newContact.uid

def delContact(vkaccount, vkid):
	#TODO Add exception handling
	idProfile = Profile.objects.get(uid = vkaccount)
	idContact = idProfile.contact_set.all().get(uid = vkid)
	idContact.delete()
	return idProfile.uid

def parseContact(vkaccount, vkid, boolean): 
## boolean 1 0 model preffered due to MySQL issue
## file:///usr/share/doc/python-django-doc/html/ref/models/fields.html#booleanfield
	idProfile = Profile.objects.get(uid = vkaccount)
	idContact = idProfile.contact_set.all().get(uid = vkid)
	idContact.isparsing = boolean
	idContact.save()
	return idContact.isparsing



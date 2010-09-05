from django.http import HttpResponse
from rpk082.robot.models import Status
from rpk082.robot.models import Contact
from rpk082.robot.models import Profile
from rpk082.robot.models import Comment
from django.shortcuts import render_to_response
from django.http import Http404
import libstatuses
import re

from django import template
import datetime
import time
import statistics


def is_mobile_browser(request):
	try:
		user_agent = request.META['HTTP_USER_AGENT']
	except KeyError:
		return False
	mobile_browsers = [r'Opera Mini', r'SonyEricsson', r'Nokia', r'Samsung', r'Siemens', r'Motorola', r'LG', r'Benq', r'Fly', r'Philips']
	for browser in mobile_browsers:
		if re.search(browser,user_agent,re.IGNORECASE):
			return True
	return False


def index(request):
	last_statuses = Status.objects.all().order_by('-date') [:30]
	contact_list = Contact.objects.all().order_by('name')
	return render_to_response ('robot/index.html', {'last_statuses': last_statuses, 'contact_list': contact_list})
	

def statuses(request):
	return render_to_response ('robot/statuses.html',
			{'now' : datetime.datetime.now(),
			'yesterday' : datetime.datetime.now().day-1,
			'number_of_statuses' : len(Status.objects.all()),
			})


def lastrecords(request, records):
	#records = min(30,int(records))
	last_statuses = Status.objects.all().order_by('-date') [:records]
	for status in last_statuses:
		status.number_of_comments = libstatuses.get_number_of_comments(status.id)
	return render_to_response ('robot/xhr/statuses.html', {'last_statuses': last_statuses})


def lastrecord(request, record):
	records = int(record)
	if (records < Status.objects.all().order_by('-date').count() ):
		status = Status.objects.all().order_by('-date') [records]
	else:
		raise Http404
	return render_to_response ('robot/xhr/status.html', {'status': status})


def contacts(request):
	contact_list = Contact.objects.all().order_by('name')
	return render_to_response ('robot/xhr/contacts.html', {'contact_list': contact_list})
	

def status(request,stat_id,msg = ''):
	stat = libstatuses.get_status(stat_id)
	if stat == None:
		return HttpResponse("404")
	comments = libstatuses.get_comments(stat)
	contact = libstatuses.get_contact(stat.contact.id)
	
	re_img = re.compile(r'\[img\](.*?)\[\/img\]',re.I | re.S)
	re_url = re.compile(r'\[url=(.*?)\](.*?)\[\/url\]',re.I | re.S)
	for comment in comments:
		comment.text = re.sub(r'>','&gt;',re.sub(r'<','&lt;',comment.text))
		comment.text = re.sub(re_url,r'<a href="\1">\2</a>',re.sub(re_img,r'<img src="\1">',comment.text)) #obtaining string with html-like links and images
		comment.text = re.sub('\n','<br>',comment.text)
	if is_mobile_browser(request):
		return render_to_response('robot/status_mobile.html',{'status':stat,'comments':comments,'stat_id':stat_id,'contact':contact,'msg':msg})
	else:
		return render_to_response('robot/status.html',{'status':stat,'comments':comments,'stat_id':stat_id,'contact':contact,'msg':msg})


def send_comment(request):
	if 'comment_text' and 'status_id' and 'email' in request.POST:
		if re.search(r"^[\s\n]*$",request.POST['comment_text']): #verify cooment text
			return status(request,int(request.POST['status_id']),'empty comment')
		if not re.search(r"^[\w.]+@[\w.]+\.\w+$",request.POST['email']): #verify e-mail
			return status(request,int(request.POST['status_id']),'wrong e-mail')
		if libstatuses.add_comment(request.POST['status_id'],request.POST['comment_text'],request.POST['email']) == None:
			if is_mobile_browser(request):
				return status(request,int(request.POST['status_id']),'an error occurred')
			else:
				return HttpResponse('an error occurred')
		else:
			if is_mobile_browser(request):
				return status(request,int(request.POST['status_id']),'successfully')
			else:
				return HttpResponse('successfully')
	return HttpResponse('unknown result')
	
	
def last_commented(request,records = '30'):
	comments = Comment.objects.all().order_by('-date')
	last_statuses = []
	for comment in comments:
		if not len(last_statuses) < int(records):
			break
		try:
			if not comment.status in last_statuses:
				last_statuses.append(comment.status)
				last_statuses[-1].number_of_comments = libstatuses.get_number_of_comments(last_statuses[-1].id)
		except Status.DoesNotExist:
			continue
	return render_to_response ('robot/xhr/statuses.html', {'last_statuses': last_statuses})
	
	
def statistic_charts(request):
	oldest_status = Status.objects.all().order_by('date')[1]
	oldest_date = datetime.datetime(oldest_status.date.year,oldest_status.date.month,oldest_status.date.day)
	day_delta = datetime.timedelta(1)
	tomorrow = datetime.datetime.now() + day_delta
	values = []
	if datetime.datetime.now() < oldest_date:
		return Http404()
	iterations_counter = 0
	value = 0
	while not (oldest_date.year == tomorrow.year and oldest_date.month == tomorrow.month and oldest_date.day == tomorrow.day):
		iterations_counter += 1
		if iterations_counter > 1000:
			break
		value = len(Status.objects.all().filter(date__year = oldest_date.year,date__month = oldest_date.month,date__day = oldest_date.day))
		values.append({'name':str(oldest_date.day) + '. ' + str(oldest_date.month),'value': value})
		now = datetime.datetime(2010,9,1)
		oldest_date += day_delta
	
	try:
		chart = statistics.chart(values,800,400,10,'all.png')
	except IOError:
		chart = ''
	

	contacts = Contact.objects.all()
	for contact in contacts:
		contact.number_of_statuses = libstatuses.get_number_of_statuses(contact.id)
	contacts = list(contacts)
	contacts.sort(lambda cont1, cont2: cont2.number_of_statuses - cont1.number_of_statuses)
	contacts = contacts[:15]

	return render_to_response('robot/statistics.html',{'img_all':chart,'most_active':contacts})


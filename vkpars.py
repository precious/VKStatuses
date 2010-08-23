#!/usr/bin/python
# -*- coding: utf-8 -*-
import libstatuses
import datetime
import urllib
import urllib2
import re
from get_between import get_between


class TempStatus:
	def __init__(self,uid_,status_,date_,name_):
		self.uid = uid_
		self.status = status_
		self.date = date_
		self.name = name_
	def __unicode__(self):
		return str(self.status)
	def __repr__(self):
		return '%s (%s) wrote: "%s" at %s' % (self.name,self.uid,self.status,self.date)


def sync_statuses():
	#add new statuses to database (main function of this module, other functions are utility)
	cookies = libstatuses.get_cookies()
	for currnet_cookie in cookies:
		
		filter_ = '2147292448'
		url = 'http://vk.com/newsfeed.php#filter=' + filter_
		headers = {
			'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3',
			'Cookie': currnet_cookie
			}
		req = urllib2.Request(url, None, headers)
		response = urllib2.urlopen(req)

		news_page = response.read()
		encoding = response.headers['content-type'].split('charset=')[-1]
		u_news = unicode(news_page,encoding)

		statuses_list = pars_all(u_news)

		for status in statuses_list[::-1]:
			if not libstatuses.is_contact_in_base(status.uid):
				libstatuses.add_contact(status.uid,status.name)
			if not libstatuses.is_status_in_base(status.uid,status.status,status.date):
				libstatuses.add_status(status.uid,status.status,status.date)


def pars_all(page):
	initial_date = 0
	statuses = []
	date = get_between(page,0,'<div class="feedDay">','</div>')
	while 1:
		if page.find('<div class="feedDay">',initial_date) == -1:
			break
		if initial_date != 0:
			date = get_between(page,initial_date - len('<div class="feedDay">') - 2,'<div class="feedDay">','</div>')
		fragment = get_between(page,initial_date,'<div class="feedDay">','<div class="feedDay">')
		if fragment == None:
			fragment = page[page.find('<div class="feedDay">',initial_date):]
			try:
				statuses.extend(pars_fragment(fragment,date));
			except TypeError:
				break
			break
		try:
			statuses.extend(pars_fragment(fragment,date));
		except TypeError:
			continue
		
		#searching in the next iteration will be start from the character with number:
		initial_date = page.find('<div class="feedDay">',page.find('<div class="feedDay">',initial_date) + 1)
	return statuses


def pars_status(page, initial):
	#extract status, uid & name from vk-page, all news except statuses must be disabled
	if page.find('feedStory',initial) == -1:
		return '', '', '', ''
	string = get_between(page, initial,'<td class="feedStory">','</td>')
	string_regexp = re.compile(r'href="/(?P<uid>.+?)">(?P<name>.+?)</a>(?P<status_with_whitespaces>.*?)(<div|$)',re.DOTALL)
	string_match = string_regexp.search(string)
	if string_match == None:
		print 'invalid status format'
		return '0','0','0','0'
	
	uid = string_match.group('uid')
	name = string_match.group('name')
	status = re.sub(r'\s*$','',re.sub(r'^\s*','',string_match.group('status_with_whitespaces'))) #remove leftmost and rightmost whitespaces

	if len(status) == 0:
		return '0','0','0','0'
	
	time = get_between(get_between(page,initial,'<td class="feedTime">','</td>'),0,'<div>','</div>')
	
	return uid, name, status, time


def pars_fragment(fragment,date):
	initial = 0
	
	date_regexp = re.compile(r"(?P<month>[A-z][a-z]+) (?P<day>\d{2}), (?P<year>\d{4})")
	date_match = date_regexp.search(date)
	if date_match == None:
		print 'invalid date format'
		return None
	
	monthes = ['January','February','March','April','May','June','July','August','September','October','November','December']
	try:
		month = monthes.index(date_match.group('month')) + 1
	except ValueError:
		print 'invalid date format [unknown month]'
		return None
	
	day = date_match.group('day')
	year = date_match.group('year')
	statuses = []
	while 1:
		uid, name, status, time = pars_status(fragment, initial)
		if name == '' or uid == '':
			break			

		if time != '0':
			hours = int(time[:time.find(':')])
			minutes = time[time.find(':') + 1:time.find('&nbsp;')]
			if time.find('p.m.') != -1 and hours < 12:
				hours += 12
			if time.find('a.m.') != -1 and hours == 12:
				hours = 0
			date_time = datetime.datetime(int(year),int(month),int(day),hours,int(minutes))
			statuses.append(TempStatus(uid,status,date_time,name))
		#searching in the next iteration will be start from the character with number:
		initial = fragment.find('<td class="feedStory">',fragment.find('<td class="feedStory">',initial) + 1)
	return statuses

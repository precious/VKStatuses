# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import auth
from django.shortcuts import render_to_response
from rpk082.exercise.models import Exercise
from rpk082.exercise.models import DayExercise
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import User

root_url = 'exercise'


def login(request):
	if request.user.is_authenticated():
		return redirect('/' + root_url + '/')
	if 'login' in request.POST and 'password' in request.POST:
		login = request.POST['login']
		password = request.POST['password']
	else:
   		return render_to_response("exercise/login.html",{"msg": "wrong authentication request","user": request.user})
   	user = auth.authenticate(username = login, password = password)
	if user is not None and user.is_active:
		auth.login(request, user)
		return redirect('/' + root_url + '/')
	else:
		return render_to_response("exercise/login.html",{"msg": "incorrect login or password","user": request.user})
		

def logout(request):
	auth.logout(request)
	return redirect('/' + root_url + '/')
	
	
def get_user_exercises(user,init_date,final_date):
	exercises = []
	delta = timedelta(1)
	while final_date > init_date:
		exercises.append({"exercises": DayExercise.objects.filter(
											username = user,
											date__year = final_date.year,
											date__month = final_date.month,
											date__day = final_date.day ).order_by('-date'),
						"date": final_date})
		final_date -= delta
	return exercises


#decorator:
def check_login(f):
	def checked(request):		
		if request.user.is_authenticated():
			return f(request)
		else:
			return render_to_response("exercise/login.html",{"user": request.user})
	return checked


@check_login
def home_page(request):
	days_number = 10
	return render_to_response("exercise/user_page.html",
								{"username": request.user.username,
								"exercises": Exercise.objects.all(),
								"dates": get_user_exercises(request.user,datetime.now() - timedelta(days_number),datetime.now()),
								"user": request.user})


@check_login
def add(request):
	exe = Exercise.objects.all()
	for exercise in exe:
		if exercise.name in request.POST:
			try:
				count = int(request.POST[exercise.name])
			except ValueError:
				continue
			day_exe = DayExercise(date = datetime.now(),name = exercise,count = count,username = request.user)
			day_exe.save()
	return redirect('/' + root_url + '/')
	

@check_login
def all_users(request):
	if "group_by" in request.GET and request.GET["group_by"] == "user":
		users = []
		days_number = 5
		for user in User.objects.all():
			users.append({"username": user.username,
						"dates": get_user_exercises(user,datetime.now() - timedelta(days_number),datetime.now())})
		return render_to_response("exercise/all_users.html",{"users": users,"user": request.user,"group_by": "user"})
	elif "group_by" in request.GET and request.GET["group_by"] == "date":
		dates = []
		days_number = 5
		day = datetime.now()
		delta = timedelta(1)
		final = day - timedelta(days_number)
		while day > final:
			dates.append({"date": day,"users": []})
			for user in User.objects.all():
				dates[-1]["users"].append({"username": user.username,
											"exercises": DayExercise.objects.filter(
													username = user,
													date__year = day.year,
													date__month = day.month,
													date__day = day.day).order_by('-date')  })
			day -= delta
		return render_to_response("exercise/all_users.html",{"dates": dates,"user": request.user,"group_by": "date"})
	else:
		return redirect('/' + root_url + '/')
		
		

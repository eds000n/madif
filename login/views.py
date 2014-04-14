from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
# Create your views here.
#class IndexView(forms.Form):
#	user = forms.CharFeld()
#	password = forms.CharField(widget=forms.Textarea)_
#	def 
def index(request):
	return render(request, 'login/index.html')
def loginForm(request):
	username = request.POST['user']
	password = request.POST['pass']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return redirect('/updata')
		else:
			return render(request, "login/index.html" )
	else:
		context = {'error_login': "error"}
		return render(request, "login/index.html", context )
		#return render('{"error_login":"error"}', mimetype='application/json' )
		##return HttpResponse('{"error_login":"error"}', mimetype='application/json' )

		

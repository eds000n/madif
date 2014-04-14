from django import http
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core import serializers
from django.core.serializers.python import Serializer
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from updata.models import Experiment, Instrument, ExpIns
import subprocess, shutil, os
# Create your views here.

class IndexView(generic.ListView):
	model = Experiment
	template_name = 'updata/index.html'
	instrument_list = Instrument.objects.all()
	def get_queryset(self):
		return Instrument.objects.all()

	@method_decorator(login_required)
	def dispatch(self, *args,  **kwargs):
		return super(IndexView, self).dispatch(*args, **kwargs)

@login_required
def upload(request):
	try:
		desc = request.POST['desc']
		perm = request.POST['permission']
		ins = request.POST['ins']
		exp = request.POST['exp']
	except:
		return HttpResponse('{"error_message":"No file"}', mimetype='application/json')
	else:
		scriptOut = ''
		for ff in request.FILES.getlist('archivo'):
			scriptOut += handleFileUpload(ff,request.session.session_key)
		#return HttpResponse('{"message":"'+scriptOut+'"}', mimetype='application/json')
		return HttpResponse(scriptOut)

@login_required
def process(request):
	try:
		desc = request.POST['desc']
		perm = request.POST['permission']
		ins = request.POST['ins']
		exp = request.POST['exp']
	except:
		return HttpResponse('{"error_message":"Wrong post params"}',mimetype='application/json')
	else:
		ei = ExpIns.objects.filter(experiment__id=exp, instrument__id=ins)
		if not ei:
			return HttpResponse('{"error_message":"wrong experiment-instrument combination"}', mimetype='application/json')
		e = Experiment.objects.filter(id=exp)
		scriptOut = execScript(desc, perm, e[0].experimentTitle, e[0].optChar, request.session.session_key)
		return HttpResponse('{"message":"'+str(scriptOut)+'"}', mimetype='application/json')

def handleFileUpload(f, ses):
	if parseFileName(f.name) == False:
		return "Error de nombre de archivo"
	folder = "uploads/"+ses
	if not os.path.exists(folder):
		os.mkdir(folder)
	with open(folder+"/"+f.name, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	return f.name+"("+str(f.size)+" bytes)<br>"

def execScript(desc, perm, expTitle, optChar,ses):
	basepath="/usr/local/madrigal/bin/python /var/www/cgi-bin/madrigal/"
	madPath="uploads/"+ses
	cmd=basepath+'createExpWithDir.py --madPath='+madPath+' --expTitle=\"'+expTitle+'\" --permission='+perm+' --fileDesc=\"'+desc+'\" --optChar=\"'+optChar+'"'
	##cmd=basepath+'createExpWithDir.py --madPath='+madPath+' --expTitle='+expTitle+' --permission='+perm+' --fileDesc='+desc+' --optChar='+optChar
	#return subprocess.check_output("echo "+cmd,shell=True)
	##return cmd
	#madOut = subprocess.check_output(cmd,shell=True).replace('\n',"<br>")
	f = open(madPath+".weblog", "wb")
	madOut = subprocess.call(cmd,stdout=f,shell=True)
	f.close()
	deleteFiles(ses)
	#return madOut.replace('"',"")
	return madOut

def parseFileName(filename):
	try:
		inst = Instrument.objects.get(mnemonic=filename[0:3]) #FIXME: should be done with regex
	except:
		return False
	date = filename[3:11]#FIXME: verificar que sea fecha correcta, x ejemplo 20019999 no debe pasar
	return True 

@login_required
def getExperiments(request):
	ins_id = request.GET['instrumentid']
	qs = Experiment.objects.filter(expins__instrument=ins_id)
	data = serializers.serialize('json',qs, fields=('experimentTitle','id'))
	return HttpResponse(data, mimetype='application/json')

def logout_view(request):
	deleteFiles(request.session.session_key)
	logout(request)
	return redirect('/login')

def deleteFiles(ses):
	folder = os.path.abspath('uploads/'+ses)
	try:
		shutil.rmtree(folder)
	except:
		return False
	#else:
	#	if not os.path.exists(folder):
	#		os.makedirs(folder)

@login_required
def consolelog(request):
	logfile = "uploads/"+request.session.session_key+".weblog"
	try :
		offset = request.GET['offset']
		f = open(logfile, 'r')
	except:
		return HttpResponse('{"data":"","offset":0}', mimetype='application/json')
	else:
		f.seek(int(offset))
		line = f.readline()
		te = f.tell()
		f.close()
		line=line.replace('"',"")
		data = '{"data":"'+line.replace('\n',"<br>")+'","offset":"'+str(te)+'"}'
		return HttpResponse(data, mimetype='application/json')

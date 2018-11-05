from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.views.generic import RedirectView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
import re
NAME_REGEX=re.compile('[A-Za-z\s]+')
EMAIL_REGEX=re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
# Create your views here.
def generate_username(name):
	count=1
	check=name
	while User.objects.filter(username=check).count()!=0:
		print(check)
		check=name+str(count)
		count=count+1
	return check
def escalatetick(request,id):
	employee = Employee.objects.filter(emp_id=request.user.id).first()
	employee.count=employee.count-1
	employee.save()
	currentlevel = employee.level
	employee=Employee.objects.all().filter(level=currentlevel+1,client_id=employee.client_id).order_by('count').first()
	employee.count=employee.count+1
	current_holder=employee.emp_id
	current_holder_name = employee.name
	current_holder_email=employee.email
	Ticket.objects.filter(id=id).update(current_holder=current_holder,current_holder_name=current_holder_name,current_holder_email=current_holder_email)
	ticket = Ticket.objects.filter(id=id).first()
	employee.save()
	subject1='Ticket Escalated Succesfully'
	message='Your ticket has been Escalated'+'\n'
	message+='Subject: '+subject1+'\n'
	message+='Ticket id :'+str(ticket.id)+'\n'
	message+='Ticket Details:'+'\n'
	message+='Creation Time:'+ '\n'+str(ticket.raised_time)+"\n"
	message+='Current Holder name : '+ current_holder_name+'\n'
	message+='Current Holder email id: '+ current_holder_email+'\n'
	email_from = settings.EMAIL_HOST_USER
	recipient_list = []
	recipient_list.append(str(request.user.email))
	print(recipient_list)
	print(send_mail(subject1,message,'mobilemoth@gmail.com',recipient_list,fail_silently=False))
	return HttpResponseRedirect(reverse("employee"))
	#return render(request,"employee.html",{'tickets':Ticket.objects.all().filter(current_holder=request.user.id)})
def closetick(request,id):
	if request.user.first_name=="user":
		Ticket.objects.filter(id=id).delete()
		return HttpResponseRedirect(reverse("user"))
	else:
		Ticket.objects.filter(id=id).delete()
		return HttpResponseRedirect(reverse("employee"))

def home(request):
	if request.user.first_name=="client":
		return HttpResponseRedirect(reverse("client"))
	if request.user.first_name=="user":
		return HttpResponseRedirect(reverse("user"))
	print(request.user.first_name)
	return HttpResponseRedirect(reverse("employee"))

def client(request):
	try:
		client = Client.objects.filter(client_id=request.user.id)
	except:
		client=None
	try:
		employees = Employee.objects.filter(client_id=request.user.id)
	except:
		employees=None
	if client==None:
		client=False
	else:
		client=True
	return render(request,"client.html",{'employees':employees,'client':client})
def deleteemp(request,pk):
	Employee.objects.all().filter(id=pk).delete()
	try:
		client = Client.objects.filter(client_id=request.user.id)
	except:
		client=None
	try:
		employees = Employee.objects.filter(client_id=request.user.id)
	except:
		employees=None
	if client==None:
		client=False
	else:
		client=True
	return redirect('client')
def user(request):
	try:
		tickets = Ticket.objects.all().filter(by=request.user.id)
	except:
		tickets=None
	return render(request,"user.html",{'tickets':tickets,'clients':Client.objects.all()})
def employee(request):
		try:
			
			tickets = Ticket.objects.all().filter(current_holder=request.user.id)
		except:
			tickets=None
		return render(request,"employee.html",{'tickets':tickets})
def addEmp(request):
	if request.method=='POST':
		errors = []
		name = request.POST.get('name')
		if NAME_REGEX.fullmatch(name)==None:
			errors.append('Name should contain only alphabets and spaces!')
			return render(request,"addEmployee.html",{'errors':errors})
		print(NAME_REGEX.fullmatch(name))
		username = generate_username(name)
		password=User.objects.make_random_password()
		email = request.POST.get('email')
		level=request.POST.get('level')
		user = User.objects.create_user(
				username = username,
				password = password,
				email = email,
				first_name="employee",
			)
		user.save()
		print(request.user.id)
		employee=Employee(name=name,emp_id=user.id,password=password,client_id=request.user.id,client_name=request.user.username,level=level,email=email)
		employee.save()
		employees = Employee.objects.all().filter(client_id=request.user.id)
		subject='Employee ID Generated'
		message='Hello '+employee.name+'!'+'\n'
		message+='Welcome to ESCCOM Family!'+'\n'
		message+='Your Account has been Succesfully generated in the portal'+'\n'
		message+='Your Login id :'+username+'\n'
		message+='Your Password :'+password+'\n'
		message+='\n'+'\n'+'Regards,\n'+'ESCCOM'+'\n'
		to=[]
		to.append(employee.email)
		send_mail(subject,message,'mobilemoth@gmail.com',to)
		return render(request,"client.html",{'answer':'Employee Added Succesfully!','employees':employees})
	return render(request,"client.html",{'answer':'Employee Not Added!','employees':employees})
def addEmployee(request):
	return render(request,"addEmployee.html",{'errors':[]})
def raisetick(request):
	subject = request.POST.get('subject')
	desc = request.POST.get('desc')
	client=int(request.POST.get('client'))
	employee=Employee.objects.all().filter(level=1,client_id=client).order_by('count').first()
	employee.count=employee.count+1
	current_holder=employee.emp_id
	current_holder_name = employee.name
	current_holder_email=employee.email
	
	ticket = Ticket(client=client,by=request.user.id,subject=subject,level=1,description=desc,current_holder=current_holder,current_holder_name=current_holder_name)
	tickets = Ticket.objects.all().filter(by=request.user.id)
	ticket.save()
	employee.save()
	subject1='Ticket raised Succesfully'
	message='Your ticket has been raised'+'\n'
	message+='Subject: '+subject+'\n'
	message+='Ticket id :'+str(ticket.id)+'\n'
	message+='Ticket Details:'+'\n'
	message+='Creation Time:'+ '\n'+str(ticket.raised_time)+"\n"
	message+='Current Holder name : '+ current_holder_name+'\n'
	message+='Current Holder email id: '+ current_holder_email+'\n'
	email_from = settings.EMAIL_HOST_USER
	recipient_list = []
	recipient_list.append(str(request.user.email))
	print(recipient_list)
	print(send_mail(subject1,message,'mobilemoth@gmail.com',recipient_list,fail_silently=False))
	return HttpResponseRedirect(reverse("user"))
 
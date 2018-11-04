from django.shortcuts import render
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .forms import UserCreateForm
# Create your views here.
def display(request,entry):
	return render(request,'display',{'entry':entry})
def signup(request):
	if request.method == 'POST':
		form = UserCreateForm(request.POST)
		if  form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			rawpassword = form.cleaned_data.get('password1')
			user = authenticate(username=username,password1=rawpassword)
			print(user)
			return redirect('login')
	else:
		form=UserCreateForm()
	return render(request,'signup.html',{'form':form})
def login(request):
	return render(request,'login.html')
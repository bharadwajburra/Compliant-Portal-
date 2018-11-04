from django.db import models

# Create your models here.
class Client(models.Model):
	name = models.CharField(max_length=100,default=None)
	client_id=models.IntegerField(default=0)
class Employee(models.Model):
	name = models.CharField(max_length=100,default=None)
	client_id = models.IntegerField(default=None)
	client_name = models.CharField(max_length=100,default=None)
	level = models.IntegerField(default=None)
	email = models.EmailField(max_length=70,blank=True, null= True,default=None)
	count = models.IntegerField(default=0)
	password = models.CharField(max_length=100,default=None)
	emp_id=models.IntegerField(default=0)

class Ticket(models.Model):
	by = models.IntegerField(default=None)
	subject = models.CharField(max_length=100,default=None)
	description=models.CharField(max_length=100,default=None)
	current_holder=models.IntegerField()
	level = models.IntegerField(default=0)
	current_holder_name = models.CharField(max_length=100,default=None)
	current_holder_email = models.EmailField(max_length=70,blank=True,null=True,default=None)
	raised_time = models.DateTimeField(auto_now_add = True)
	client = models.IntegerField(default=0)
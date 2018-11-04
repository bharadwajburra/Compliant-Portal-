"""Mini URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from clients import views
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
urlpatterns = [
   url(r'^$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
   url(r'^home$',views.home,name='home'),
   url(r'^client$',views.client,name='client'),
   url(r'^user$',views.user,name='user'),
   url(r'^addEmp$',views.addEmp,name='addEmp'),
   url(r'^addEmployee$',views.addEmployee,name='addEmployee'),
   url(r'^employee$',views.employee,name='employee'),
   url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
   url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
   url(r'^signup/$', accounts_views.signup, name='signup'),
   url(r'^raise/(?P<pk>\d+)/$',views.raisetick,name='raiseticket'),
   url(r'^closetick/(?P<id>\d+)/$',views.closetick,name='closetick'),
   url(r'^escalate/(?P<id>\d+)/$',views.escalatetick,name='escalate'),
   url(r'^deleteEmp/(?P<pk>\d+)/$',views.deleteemp,name='deleteemp'),
   url(r'^admin/',admin.site.urls),
]

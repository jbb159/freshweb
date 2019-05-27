"""dailyfresh URL Configuration

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
from django.conf.urls import url,include
import user.views
import goods.views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^user/register$',user.views.register.as_view()),
    url(r'goods/index',goods.views.index,name='shouye'),
    url(r'^user/active/(.*?)$',user.views.active),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^user/login$',user.views.login.as_view(),name='denglu'),
    url(r'^b$',user.views.b),
    url(r'^user/info$',user.views.usercenterinfo),
    url(r'^user/site$',user.views.usercentersite),
    url(r'^user/order$',user.views.usercenterorder),
]

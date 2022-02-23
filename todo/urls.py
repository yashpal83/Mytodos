from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('about', views.about, name = "about"),
    path('delete/<int:num>', views.delete, name = "delete"),
    path('update/<int:num>', views.update, name = "update"),
    path('contact', views.contact, name = "contact"),
    path('search', views.search, name = "search"),
    path('login', views.handlelogin, name = "handlelogin"),
    path('signup', views.handlesignup, name = "handlesignup"),
    path('logout', views.handlelogout, name = "handlelogout")

    
]

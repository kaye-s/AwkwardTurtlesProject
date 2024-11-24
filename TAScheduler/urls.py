
from django.contrib import admin
from django.urls import path
from TAScheduler.views import AccountManagementView
from TAScheduler.views import Login

urlpatterns = [
    path('admin/', admin.site.urls),
    #Temporarily routing home page as Account Management so we can see what it looks like
    path('',Login.as_view()),
    path('AccountManagement/',AccountManagementView.as_view()),
]
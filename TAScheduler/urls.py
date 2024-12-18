from django.urls import path
from TAScheduler.views import AccountManagementView, CustomLoginView
from django.contrib.auth.views import LogoutView
from TAScheduler.views import Courses_Supervisor


urlpatterns = [
    path("", CustomLoginView.as_view(), name="login"),
    path("account-management/", AccountManagementView.as_view(), name="account-management"),

    path("logout/",LogoutView.as_view(), name="logout"),

    path('courses/', Courses_Supervisor.as_view(), name='courses-supervisor'),

]
from django.urls import path
from TAScheduler.views import AccountManagementView, CustomLoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("", CustomLoginView.as_view(), name="login"),
    path("account-management/", AccountManagementView.as_view(), name="account-management"),
    path("logout/",LogoutView.as_view(), name="logout")
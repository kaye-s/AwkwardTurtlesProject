from django.urls import path
from TAScheduler.views import AccountManagementView


urlpatterns = [
    path("account-management/", AccountManagementView.as_view(), name="account-management"),
]
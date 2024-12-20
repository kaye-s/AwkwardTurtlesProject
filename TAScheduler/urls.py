from django.urls import path
from TAScheduler.views import AccountManagementView, CustomLoginView, courses_other, AccountOtherView
from django.contrib.auth.views import LogoutView
from TAScheduler.views import Courses_Supervisor, create_course, edit_course, delete_course
from TAScheduler.views import ContactInfoView


urlpatterns = [
    path("", CustomLoginView.as_view(), name="login"),
    path("account-management/", AccountManagementView.as_view(), name="account-management"),

    path("account_other/", AccountOtherView.as_view(), name="account-other"),
    path("logout/",LogoutView.as_view(), name="logout"),

    #path('courses/', courses_supervisor, name='courses'),  # Add this line
    path('courses_supervisor/', Courses_Supervisor.as_view(), name='courses-supervisor'),
    # path('create_course/', create_course, name='create-course'),
    # path('edit_course/<int:course_id>/', edit_course, name='edit-course'),
    # path('delete_course/<int:course_id>/', delete_course, name='delete-course'),

    path('courses_other/', courses_other.as_view(), name='courses-other'),

    path("contact-info/", ContactInfoView.as_view(), name="contact-info"),

]
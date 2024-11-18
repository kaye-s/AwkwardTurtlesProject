from django.shortcuts import render
from django.views import View

# Create your views here.

#Simple post request in order to see formatting
class AccountManagement(View):
    def get(self,request):
        return render(request, "AccountManagement.html", {})
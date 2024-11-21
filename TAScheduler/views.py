
from django.shortcuts import render
from django.views import View

# Create your views here.

#Simple post request in order to see formatting
class AccountManagement(View):
    def get(self,request):
        return render(request, "AccountManagement.html", {})

    # POST REQUEST FOR ACCOUNT MANAGEMENT FORM
    def post(self, request):

        #something like this from parking lab to handle data
        # sec = request.POST.get('section')
        # date = request.POST.get('dateTime')

        # fill in context to handle database data
        return render(request, "AccountManagement.html", {})


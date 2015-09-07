from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.models import User

from .forms import AddOrganizationForm, AddUserForm
from .models import Organization, MSUser

# Create your views here.
def tryAgain(request, msg=None, url=None, buttonText=None,
             title=None):
    """ Helper function that provides a simple "Try Again"
        page.
    """
    if msg is None:
        msg = "Please try again"
    if url is None:
        url = "javascript:history.back()"
    if buttonText is None:
        buttonText = "Try Again"
    if title is None:
        title = "Try Again"
    context = {"msg": msg,
               "url": url,
               "button_text": buttonText,
               "title": title}
    return render(request, "dbkeeper/try_again.html", context)
    
def index(request):
    """ Display the dbkeeper home page. """
    return render(request, "dbkeeper/index.html")

class AddOrganization(View):
    context = {
               "form":   None,
               "entity": "organization",
               "submit": "Add",
              }
    
    def get(self, request):
        self.context["form"] = AddOrganizationForm()
        return render(request, "dbkeeper/add.html", self.context)
    
    def post(self, request):
        self.context["form"] = AddOrganizationForm(request.POST)
        form = self.context["form"]
        if form.is_valid():
            name = form.cleaned_data["name"]
            type = form.cleaned_data["type"]
            org = Organization(name=name, type=type)
            org.save()
            return HttpResponseRedirect("/dbkeeper/")

        return render(request, "dbkeeper/add.html", self.context)

class AddUser(View):
    context = {
               "form":   None,
               "entity": "user",
               "submit": "Add",
              }
    
    def get(self, request):
        self.context["form"] = AddUserForm()
        return render(request, "dbkeeper/add.html", self.context)
    
    def post(self, request):
        self.context["form"] = AddUserForm(request.POST)
        form = self.context["form"]
        if form.is_valid():
            # Reject input if user already exists
            username = form.cleaned_data["username"]
            if User.objects.filter(username=username).count() > 0:
                # reject
                return tryAgain(msg="The username '{}' already exists".format(username),
                                url="javascript:history.back()")
            password     = form.cleaned_data["password"]
            firstName    = form.cleaned_data["firstName"]
            lastName     = form.cleaned_data["lastName"]
            email        = form.cleaned_data["email"]
            organization = form.cleaned_data["organization"]
            mobilePhone  = form.cleaned_data["mobilePhone"]
            workPhone    = form.cleaned_data["workPhone"]
            otherPhone   = form.cleaned_data["otherPhone"]
            note         = form.cleaned_data["note"]

            # Create a Django User object
            user = User.objects.create_user(username, email=email, password=password)
            user.first_name = firstName
            user.last_name = lastName
            user.save()
            
            msUser = MSUser(organization=organization,
                            work_phone=workPhone,
                            mobile_phone=mobilePhone,
                            other_phone=otherPhone,
                            note=note,
                            user=user)
            msUser.save()

            return HttpResponseRedirect("/dbkeeper/")

        return render(request, "dbkeeper/add.html", self.context)

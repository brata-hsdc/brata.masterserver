from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.models import User

from .forms import AddOrganizationForm, AddUserForm, AddTeamForm, CheckInTeamForm,\
                   AddLaunchParamsForm, AddDockParamsForm, AddSecureParamsForm, AddReturnParamsForm
from .models import Organization, MSUser, Team, Setting
from piservice.models import PiEvent
from .team_code import TeamPassCode

import json

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
    
#----------------------------------------------------------------------------
def index(request):
    """ Display the dbkeeper home page. """
    return render(request, "dbkeeper/index.html")

#----------------------------------------------------------------------------
def test(request):
    """ Display the QR Code test page. """
    return render(request, "dbkeeper/test.html")

#----------------------------------------------------------------------------
def station_status(request):
    """ Home page view for piservice.  Since this is a service, we could
        return 404, or we could put up a helpful page with some options.
    """
    refreshInterval = Setting.get("STATION_STATUS_REFRESH_INTERVAL_MS", default="5000")
    return render(request, "dbkeeper/station_status.html",
                  {"PAGE_REFRESH_INTERVAL": refreshInterval})

#----------------------------------------------------------------------------
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
            if Organization.objects.filter(name=name).count() > 0:
                self.context["title"] = "Organization already exists"
                self.context["msg"] = """The organization '{}' already exists in the database.<br />
                                         Please press the Try Again button to go back and
                                         enter a different name.""".format(name)
                self.context["button_text"] = "Try Again"
                
                ev = PiEvent.createEvent(type=PiEvent.ADDORG_TYPE, status=PiEvent.FAIL_STATUS,
                                         message="Organization '{}' already exists".format(name))
                ev.save()

                return render(request, "dbkeeper/try_again.html", self.context)
            
            type = form.cleaned_data["type"]
            org = Organization(name=name, type=type)
            org.save()
            
            ev = PiEvent.createEvent(type=PiEvent.ADDORG_TYPE, status=PiEvent.SUCCESS_STATUS,
                                     message="Organization '{}' added".format(unicode(org)))
            ev.save()
            return HttpResponseRedirect("/dbkeeper/")

        return render(request, "dbkeeper/add.html", self.context)

#----------------------------------------------------------------------------
class AddUser(View):
    """ Add an MSUser (and a User) record to the database """
    context = {
               "form":   None,
               "entity": "user",
               "submit": "Add",
              }
    
    def get(self, request):
        """ Handle an add/user GET request (URL coming from another page) """
        self.context["form"] = AddUserForm()
        return render(request, "dbkeeper/add.html", self.context)
    
    def post(self, request):
        """ Handle an add/user POST request (form submit or resubmit) """
        self.context["form"] = AddUserForm(request.POST)
        form = self.context["form"]
        if form.is_valid():
            # Reject input if user already exists
            username = form.cleaned_data["username"]
            if User.objects.filter(username=username).count() > 0:
                # reject
                ev = PiEvent.createEvent(type=PiEvent.ADDUSER_TYPE, status=PiEvent.FAIL_STATUS,
                                         message="User '{}' already exists".format(username))
                ev.save()

                return tryAgain(msg="The username '<b>{}</b>' already exists".format(username),
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

            ev = PiEvent.createEvent(type=PiEvent.ADDUSER_TYPE, status=PiEvent.SUCCESS_STATUS,
                                     message="User '{}' added".format(unicode(msUser)))
            ev.save()
            return HttpResponseRedirect("/dbkeeper/")

        return render(request, "dbkeeper/add.html", self.context)

#----------------------------------------------------------------------------
class AddTeam(View):
    context = {
               "form":   None,
               "entity": "Team",
               "submit": "Add",
              }
    
    def get(self, request):
        self.context["form"] = AddTeamForm()
        return render(request, "dbkeeper/add.html", self.context)
    
    def post(self, request):
        self.context["form"] = AddTeamForm(request.POST)
        form = self.context["form"]
        if form.is_valid():
            name = form.cleaned_data["name"]
            if Team.objects.filter(name=name).count() > 0:
                self.context["title"] = "Organization already exists"
                self.context["msg"] = """The team '<b>{}</b>' already exists in the database.<br/>
                                         Please press the Try Again button to go back and
                                         enter a different name.""".format(name)
                self.context["button_text"] = "Try Again"
                ev = PiEvent.createEvent(type=PiEvent.ADDTEAM_TYPE, status=PiEvent.FAIL_STATUS,
                                         message="Team '{}' already exists".format(name))
                ev.save()
                return render(request, "dbkeeper/try_again.html", self.context)
            
            org = form.cleaned_data["organization"]
            team = Team(name=name, organization=org)
            team.pass_code = team.makeTeamCode(list(Team.objects.values_list("pass_code")))
            team.save()
            
            ev = PiEvent.createEvent(type=PiEvent.ADDTEAM_TYPE, status=PiEvent.SUCCESS_STATUS, team=team,
                                     message="Team '{}' added".format(unicode(team)))
            ev.save()
            return HttpResponseRedirect("/dbkeeper/")

        return render(request, "dbkeeper/add.html", self.context)

#----------------------------------------------------------------------------
class CheckInTeam(View):
    """ Check a Team in for the competition.
        This View class checks a Team in for the competition by verifying
        that the Team exists, and that the entered team code matches the
        team code in the database.
        
        Team CheckIn is distinct from BRATA Registration.  Team CheckIn
        authenticates the Team to use the TeamCentral site to see their
        stats.
        
        This will need to be modified from its current state.  Maybe it
        should just use the Django authentication mechanism.
    """
    context = {
               "form":   None,
               "title":  "Team Check-In",
               "entity": "Team",
               "submit": "Add",
              }
    
    def get(self, request):
        """ Handle an add/user GET request (URL coming from another page) """
        self.context["form"] = CheckInTeamForm()
        return render(request, "dbkeeper/check_in.html", self.context)
        
    def post(self, request):
        """ Handle an add/user POST request (form submit or resubmit) """
        self.context["form"] = CheckInTeamForm(request.POST)
        form = self.context["form"]
        if form.is_valid():
            team = form.cleaned_data["team"]
            code = "{}{}{}{:02}".format(form.cleaned_data["teamCode1"],
                                        form.cleaned_data["teamCode2"],
                                        form.cleaned_data["teamCode3"],
                                        int(form.cleaned_data["teamCode4"]))
            
            if not code or code != team.pass_code:
                self.context["title"] = "Invalid Team Code"
                self.context["msg"] = """The code '<b>{}</b>' is either not a valid code or is not
                                         the code assigned to your team.<br/>
                                         Please press the Try Again button to go back and
                                         enter a different code.""".format(TeamPassCode.wordify(code))
                self.context["button_text"] = "Try Again"
                
                ev = PiEvent.createEvent(type=PiEvent.CHECKIN_TYPE, status=PiEvent.FAIL_STATUS, team=team,
                                         message="Team '{}' invalid team code '{}'.".format(team.name, code))
                ev.save()
            
                return render(request, "dbkeeper/try_again.html", self.context)
            
            # If we reach here, the code is correct, so check the team in
            # by generating a CHECKIN event
            ev = PiEvent.createEvent(type=PiEvent.CHECKIN_TYPE, status=PiEvent.SUCCESS_STATUS, team=team,
                                     message="Team '{}' checked in".format(unicode(team)))
            ev.save()
            
            return HttpResponseRedirect("/dbkeeper/")
        
        # Form was not valid, so let the user update fields and resubmit
        return render(request, "dbkeeper/check_in.html", self.context)

#----------------------------------------------------------------------------
class AddLaunchParams(View):
    context = {
               "form":   None,
               "entity": "LaunchParams",
               "submit": "Add",
              }
    
    def get(self, request):
        """ Display the Add form with the AddLaunchParams fields """
        try:
            launchParams = Setting.getLaunchParams()
            d = {}
            for tri,color in ((0,"r"), (1,"g"), (2,"b")):
                for vert in (0, 1, 2):
                    v = color + "v{}".format(vert)
                    name,lat,lon,angle = launchParams[tri][vert]
                    d[v + "name"]  = name
                    d[v + "lat"]   = lat
                    d[v + "lon"]   = lon
                    d[v + "angle"] = angle
                cname,sidelen = launchParams[tri][3]
                d[color + "vcname"]  = cname
                d[color + "sidelen"] = sidelen
            self.context["form"] = AddLaunchParamsForm(initial=d)
        except:
            self.context["form"] = AddLaunchParamsForm()
        return render(request, "dbkeeper/add_launch_params.html", self.context)
    
    def post(self, request):
        self.context["form"] = AddLaunchParamsForm(request.POST)
        form = self.context["form"]
        if form.is_valid():
            # Create a more structured JSON object
#             value = json.dumps(form.cleaned_data)
            d = form.cleaned_data
            redTri   = ((d["rv0name"], d["rv0lat"], d["rv0lon"], d["rv0angle"]),
                        (d["rv1name"], d["rv1lat"], d["rv1lon"], d["rv1angle"]),
                        (d["rv2name"], d["rv2lat"], d["rv2lon"], d["rv2angle"]),
                        (d["rvcname"], d["rsidelen"]),
                       )
            greenTri = ((d["gv0name"], d["gv0lat"], d["gv0lon"], d["gv0angle"]),
                        (d["gv1name"], d["gv1lat"], d["gv1lon"], d["gv1angle"]),
                        (d["gv2name"], d["gv2lat"], d["gv2lon"], d["gv2angle"]),
                        (d["gvcname"], d["gsidelen"]),
                       )
            blueTri  = ((d["bv0name"], d["bv0lat"], d["bv0lon"], d["bv0angle"]),
                        (d["bv1name"], d["bv1lat"], d["bv1lon"], d["bv1angle"]),
                        (d["bv2name"], d["bv2lat"], d["bv2lon"], d["bv2angle"]),
                        (d["bvcname"], d["bsidelen"]),
                       )
            value = json.dumps((redTri, greenTri, blueTri,))
            try:
                setting = Setting.objects.get(name="LAUNCH_PARAMS")
                setting.value = value
            except Setting.DoesNotExist:
                setting = Setting(name="LAUNCH_PARAMS", value=value, description="Competition parameters for the Launch challenge")
            setting.save()
            return HttpResponseRedirect("/admin/dbkeeper/setting/")

        return render(request, "dbkeeper/add_launch_params.html", self.context)

#----------------------------------------------------------------------------
class AddDockParams(View):
    context = {
               "form":   None,
               "entity": "DockParams",
               "submit": "Add",
              }
    
    def get(self, request):
        """ Display the Add form with the AddDockParams fields """
        self.context["form"] = AddDockParamsForm()
        return render(request, "dbkeeper/add.html", self.context)
    
    def post(self, request):
        self.context["form"] = AddDockParamsForm(request.POST)
        form = self.context["form"]
        if form.is_valid():
            value = json.dumps(form.cleaned_data)
            try:
                setting = Setting.objects.get(name="DOCK_PARAMS")
                setting.value = value
            except Setting.DoesNotExist:
                setting = Setting(name="DOCK_PARAMS", value=value, description="Competition parameters for the Dock challenge")
            setting.save()
            return HttpResponseRedirect("/admin/dbkeeper/setting/")

        return render(request, "dbkeeper/add.html", self.context)

#----------------------------------------------------------------------------
class AddSecureParams(View):
    context = {
               "form":   None,
               "entity": "SecureParams",
               "submit": "Add",
              }
    
    def get(self, request):
        """ Display the Add form with the AddSecureParams fields """
        self.context["form"] = AddSecureParamsForm()
        return render(request, "dbkeeper/add.html", self.context)
    
    def post(self, request):
        self.context["form"] = AddSecureParamsForm(request.POST)
        form = self.context["form"]
        if form.is_valid():
            value = json.dumps(form.cleaned_data)
            try:
                setting = Setting.objects.get(name="SECURE_PARAMS")
                setting.value = value
            except Setting.DoesNotExist:
                setting = Setting(name="SECURE_PARAMS", value=value, description="Competition parameters for the Secure challenge")
            setting.save()
            return HttpResponseRedirect("/admin/dbkeeper/setting/")

        return render(request, "dbkeeper/add.html", self.context)

#----------------------------------------------------------------------------
class AddReturnParams(View):
    context = {
               "form":   None,
               "entity": "ReturnParams",
               "submit": "Add",
              }
    
    def get(self, request):
        """ Display the Add form with the AddReturnParams fields """
        self.context["form"] = AddReturnParamsForm()
        return render(request, "dbkeeper/add.html", self.context)
    
    def post(self, request):
        self.context["form"] = AddReturnParamsForm(request.POST)
        form = self.context["form"]
        if form.is_valid():
            value = json.dumps(form.cleaned_data)
            try:
                setting = Setting.objects.get(name="RETURN_PARAMS")
                setting.value = value
            except Setting.DoesNotExist:
                setting = Setting(name="RETURN_PARAMS", value=value, description="Competition parameters for the Return challenge")
            setting.save()
            return HttpResponseRedirect("/admin/dbkeeper/setting/")

        return render(request, "dbkeeper/add.html", self.context)


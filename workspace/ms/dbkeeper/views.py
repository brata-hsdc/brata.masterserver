from django.shortcuts import render, HttpResponseRedirect, HttpResponse, Http404
from django.views.generic import View
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from .forms import AddOrganizationForm, AddUserForm, AddTeamForm, CheckInTeamForm,\
                   AddLaunchParamsForm, AddDockParamsForm, AddSecureParamsForm, AddReturnParamsForm,\
                   LoadSettingsForm, CompetitionStartForm, CompetitionEndForm, LogMessageForm,\
                   ReturnTestForm
from .models import Organization, MSUser, Team, Setting
from piservice.models import PiEvent
from .team_code import TeamPassCode

import json
import random
import csv
import operator
from datetime import date as Date
from cStringIO import StringIO


#-------------------------
# Useful helper functions
#-------------------------

#----------------------------------------------------------------------------
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
def schoolNameFromPassCode(pass_code):
    """ Given a team pass_code, return the school name.
    
        Returns:  the school name, or None if not found.
    """
    try:
        return Team.objects.get(pass_code=pass_code).organization.name
    except Team.DoesNotExist:
        return None

#-------------------------
# Create your views here.
#-------------------------

#----------------------------------------------------------------------------
@login_required
def index(request):
    """ Display the dbkeeper home page. """
    return render(request, "dbkeeper/index.html")

#----------------------------------------------------------------------------
class regtest(View):
    """ Display the QR Code test page. """
    #queryset = Team.objects.all()
    #table = RegTable(queryset)
    #return render_to_response("dbkeeper/regtest.html", {"table": table}, context_instance=RequestContext(request))
    context = {
               "table":   None,
              }
    
    def get(self, request):
        teams = Team.objects.all().order_by("organization__name","name")
        #self.context["table"] = teams
        
        # Join the teams with the launch test points for each school
        launchTestPoints = json.loads(Setting.objects.get(name="LAUNCH_TEST_DATA").value)
        table = []    
        for team in teams:
            if team.organization.name in launchTestPoints:
                entry = {}
                entry["organization"] = team.organization.name  # school name
                entry["name"] = team.name  # team name
                entry["pass_code"] = team.pass_code
                entry["points"] = launchTestPoints[team.organization.name]
                table.append(entry)
        self.context["table"] = table
        
        # Get the URL of the DOCK_TEST_HOST
        self.context["dock_test_host"] = Setting.objects.get(name="DOCK_TEST_HOST").value
        return render(request, "dbkeeper/regtest.html", self.context)

#----------------------------------------------------------------------------
class regtest_team(View):
    """ Display the QR Code test page. """
    context = {
               "pass_code":   None,
              }
    
    def get(self, request, pass_code):
        msBaseUrl = request.get_host()
        #QR_SERVICE_REQUEST_URL = "http://zxing.org/w/chart?cht=qr&chs=350x350&chld=L&choe=UTF-8&chl="
        self.context["qr_service_url"] = Setting.get("MS_EXTERNAL_HOST_ADDRESS", default=msBaseUrl)+"/piservice/qrcode?chl="      
        self.context["host"] = Setting.get("MS_EXTERNAL_HOST_ADDRESS", default=msBaseUrl)
        self.context["register_url"] = reverse("register", kwargs={"team_passcode": pass_code}, current_app=request.resolver_match.app_name)
        self.context["unregister_url"] = reverse("unregister", current_app=request.resolver_match.app_name)
        self.context["reset_url"] = reverse("reset", kwargs={"team_passcode": pass_code}, current_app=request.resolver_match.app_name)
        self.context["pass_code"] = pass_code
        return render(request, "dbkeeper/regtest_team.html", self.context)

#----------------------------------------------------------------------------
class NavTestTeam(View):
    """ Display a map test page with markers. """
    context = {
               "entity":    "Launch Test",
               "pass_code": None,
               "no_sidebarLeft": True,
               "no_mainRight": True,
              }
    
    def get(self, request, pass_code, lat1, lon1, lat2, lon2, lat3, lon3, lat4, lon4, school_name):
        self.context["pass_code"] = pass_code
        # send the points to the template as an array of GeoJSON objects
        pt0 = '{{ "x": {}, "y": {} }}'.format(lon1, lat1)  # red
        pt1 = '{{ "x": {}, "y": {} }}'.format(lon2, lat2)  # green
        pt2 = '{{ "x": {}, "y": {} }}'.format(lon3, lat3)  # blue
        pt3 = '{{ "x": {}, "y": {} }}'.format(lon4, lat4)  # yellow
        pt4 = '{{ "x": {}, "y": {} }}'.format(sum([float(x) for x in [lon1, lon2, lon3, lon4]])/4.0,  # centroid
                                              sum([float(y) for y in [lat1, lat2, lat3, lat4]])/4.0)
        self.context["points"] = "'[" + ", ".join([pt0, pt1, pt2, pt3, pt4]) + "]'";
        
        # Choose on of the points at random for the team to identify
        random.seed();
        n = random.randint(0,3)
        self.context["lat"] = (lat1, lat2, lat3, lat4)[n]
        self.context["lon"] = (lon1, lon2, lon3, lon4)[n]
        self.context["answer"] = ["Incorrect"] * 4
        self.context["answer"][n] = "Correct!"
        self.context["entity"] += " for " + school_name
        return render(request, "dbkeeper/navtest_team.html", self.context)

#----------------------------------------------------------------------------
class ReturnTestTeam(View):
    """ Display a page to collect return parameters. """
    context = {
               "entity":    "Return Test",
               "form":      None,
               "pass_code": None,
               "submit":    "Submit",
               "answer":    "",
               "school":    "<unknown school>",
               "no_sidebarLeft": True,
               "no_mainRight": True,
              }
    
    def get(self, request, pass_code):
        self.context["form"] = ReturnTestForm(label_suffix="")
        self.context["pass_code"] = pass_code
        
        schoolName = schoolNameFromPassCode(pass_code)
        if schoolName is None:
            return tryAgain(request, msg="Invalid team passcode: {}".format(pass_code), title="Invalid Passcode")
        else:
            self.context["school"] = schoolName
            
        jparams = Setting.objects.get(name="RETURN_TEST_DATA").value
        params = json.loads(jparams)
        
        # Squirrel away values in hidden fields so we can get them back in POST
        self.context["form"].fields["params"].initial = json.dumps(params[schoolName])
        self.context["form"].fields["school"].initial = schoolName
        return render(request, "dbkeeper/returntest_team.html", self.context)
    
    def post(self, request, pass_code):
        form = ReturnTestForm(request.POST, label_suffix="")
        self.context["form"] = form
        self.context["pass_code"] = pass_code

        if form.is_valid():
            values = [ form.cleaned_data["value1"],
                       form.cleaned_data["value2"],
                       form.cleaned_data["value3"],
                       form.cleaned_data["value4"],
                       form.cleaned_data["value5"],
                       form.cleaned_data["value6"],
                     ]
            reverse = form.cleaned_data["reverse"]
            params = json.loads(form.cleaned_data["params"])[1 if reverse else 0]

            match = reduce(operator.__and__, [a==b for a,b in zip(values, params)])
            if match:
                self.context["answer"] = "Correct!"
            else:
                self.context["answer"] = "Incorrect"
        else:
            self.context["answer"] = "Each value must be exactly 2 decimal digits"
        return render(request, "dbkeeper/returntest_team.html", self.context)
        

#----------------------------------------------------------------------------
@login_required
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
    
    @method_decorator(login_required)
    def get(self, request):
        self.context["form"] = AddOrganizationForm()
        return render(request, "dbkeeper/add.html", self.context)
    
    @method_decorator(login_required)
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
    
    @method_decorator(login_required)
    def get(self, request):
        """ Handle an add/user GET request (URL coming from another page) """
        self.context["form"] = AddUserForm()
        return render(request, "dbkeeper/add.html", self.context)
    
    @method_decorator(login_required)
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
    
    @method_decorator(login_required)
    def get(self, request):
        self.context["form"] = AddTeamForm()
        return render(request, "dbkeeper/add.html", self.context)
    
    @method_decorator(login_required)
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
    
    @method_decorator(login_required)
    def get(self, request):
        """ Handle an add/user GET request (URL coming from another page) """
        self.context["form"] = CheckInTeamForm()
        return render(request, "dbkeeper/check_in.html", self.context)
        
    @method_decorator(login_required)
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
               "submit": "Done",
              }
    
    @method_decorator(login_required)
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
            form = self.context["form"]

        return render(request, "dbkeeper/add_launch_params.html", self.context)
    
    @method_decorator(login_required)
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
               "submit": "Done",
              }
    
    @method_decorator(login_required)
    def get(self, request):
        """ Display the Add form with the AddDockParams fields """
#         self.context["form"] = AddDockParamsForm()
#         self.context["data"] = { "sets": [
#                                           {"tape_id":"1", "tape_len":1, "a_aft":1, "a_fore":1, "f_rate":1, "f_qty":1},
#                                           {"tape_id":"2", "tape_len":2, "a_aft":2, "a_fore":2, "f_rate":2, "f_qty":2},
#                                           {"tape_id":"3", "tape_len":3, "a_aft":3, "a_fore":3, "f_rate":3, "f_qty":3},
#                                          ] }
#         return render(request, "dbkeeper/add_dock_params.html", self.context)
        form = AddDockParamsForm()
        form.setFixedFields()
        try:
            dockParams = Setting.getDockParams()
            form.setFields(len(dockParams["sets"]))
#             form.setData(dockParams)
            self.context["data"] = form.setData(dockParams)
        except:
            self.context["data"] = { "numRows": 0 }
        self.context["form"] = form
        return render(request, "dbkeeper/add_dock_params.html", self.context)
    
    @method_decorator(login_required)
    def post(self, request):
        form = AddDockParamsForm()
        form.setFixedFields()
        form.setFields(int(request.POST["numRows"]))
        form.data = request.POST
        form.is_bound = True
        form.validate(request.POST)
        if form.is_valid():
#             value = json.dumps(form.cleaned_data)
            value = form.buildStructure(form.cleaned_data)
            value = json.dumps(value)
            try:
                setting = Setting.objects.get(name="DOCK_PARAMS")
                setting.value = value
            except Setting.DoesNotExist:
                setting = Setting(name="DOCK_PARAMS", value=value, description="Competition parameters for the Dock challenge")
            setting.save()
            return HttpResponseRedirect("/admin/dbkeeper/setting/")
#         else:
#             err = form.errors

        self.context["form"] = form
        return render(request, "dbkeeper/add_dock_params.html", self.context)

#----------------------------------------------------------------------------
class AddSecureParams(View):
    context = {
               "form":   None,
               "entity": "SecureParams",
               "submit": "Done",
              }
    
    @method_decorator(login_required)
    def get(self, request):
        """ Display the Add form with the AddSecureParams fields """
        form = AddSecureParamsForm()
        #form.setFixedFields()
        try:
            secureParams = Setting.getSecureParams()
            form.setFields(len(secureParams["sets"]))
        except:
            self.context["data"] = { "numRows": 0 }
        self.context["form"] = form
        return render(request, "dbkeeper/add_secure_params.html", self.context)
    
    @method_decorator(login_required)
    def post(self, request):
        form = AddSecureParamsForm(request.POST)
        #form.setFixedFields()
        form.setFields(int(request.POST["numRows"]))
        form.data = request.POST
        form.is_bound = True
        form.validate(request.POST)
        if form.is_valid():
            value = form.buildStructure(form.cleaned_data)
            value = json.dumps(value)
            try:
                setting = Setting.objects.get(name="SECURE_PARAMS")
                setting.value = value
            except Setting.DoesNotExist:
                setting = Setting(name="SECURE_PARAMS", value=value, description="Competition parameters for the Secure challenge")
            setting.save()
            return HttpResponseRedirect("/admin/dbkeeper/setting/")
#         else:
#             err = form.errors

        self.context["form"] = form
        return render(request, "dbkeeper/add_secure_params.html", self.context)

#----------------------------------------------------------------------------
class AddReturnParams(View):
    context = {
               "form":   None,
               "entity": "ReturnParams",
               "submit": "Done",
              }
    
    @method_decorator(login_required)
    def get(self, request):
        """ Display the add_return_params form.
        
        If RETURN_PARAMS already exists in the database, the form
        is populated with the current values.
        """
#         self.context["form"] = AddReturnParamsForm()
#         return render(request, "dbkeeper/add_return_params.html", self.context)
        try:
            returnParams = Setting.getReturnParams()
            d = {}
            for station in range(0, 6):
                fields = ["st{}{}".format(station, valname) for valname in ("id", "v0", "v1", "v2", "v3", "v4", "v5")]
                values = returnParams[station]
                
                for f,v in zip(fields, values):
                    d[f] = v 

            self.context["form"] = AddReturnParamsForm(initial=d)
        except:
            self.context["form"] = AddReturnParamsForm()
        return render(request, "dbkeeper/add_return_params.html", self.context)
    
    @method_decorator(login_required)
    def post(self, request):
        self.context["form"] = AddReturnParamsForm(request.POST)
        form = self.context["form"]
        if form.is_valid():
            d = form.cleaned_data
            values = []
            for station in range(0, 6):
                fields = ["st{}{}".format(station, valname) for valname in ("id", "v0", "v1", "v2", "v3", "v4", "v5")]
                values.append([d[f] for f in fields])
            
            values = json.dumps(values)
            try:
                setting = Setting.objects.get(name="RETURN_PARAMS")
                setting.value = values
            except Setting.DoesNotExist:
                setting = Setting(name="RETURN_PARAMS", value=value, description="Competition parameters for the Return challenge")
            setting.save()
            return HttpResponseRedirect("/admin/dbkeeper/setting/")

        return render(request, "dbkeeper/add_return_params.html", self.context)

#----------------------------------------------------------------------------
@login_required
def SaveSettings(request):
    """ Display the save_settings page. """
    return render(request, "dbkeeper/save_settings.html")

#----------------------------------------------------------------------------
@login_required
def SaveSettingsConfirmed(request):
    """ Send back the CSV file """
    # Create a response object to send back the data
    response = HttpResponse(content_type="tex/plain")
    
    # Write the CSV into the response
    fieldNames = ["name", "value", "description"]
    writer = csv.DictWriter(response, fieldnames=fieldNames)
    writer.writeheader()
    for s in Setting.objects.values(*fieldNames).order_by("name"):
        writer.writerow(s)
    
    response["Content-Disposition"] = "attachment; filename=Settings_{}.csv".format(str(Date.today()))
    return response

#----------------------------------------------------------------------------
class LoadSettings(View):
    context = {
               "form":   None,
               "entity": "Load Settings from CSV",
               "submit": "Upload CSV",
              }

    @method_decorator(login_required)
    def get(self, request):
        """ Display the form """
        self.context["form"] = LoadSettingsForm()
        self.context["upload"] = True
        return render(request, "dbkeeper/load_settings.html", self.context)
    
    @method_decorator(login_required)
    def post(self, request):
        if hasattr(request, "FILES") and "loadFile" in request.FILES:
            form = LoadSettingsForm(request.POST, request.FILES)
            if form.is_valid():
                # Read the CSV file
                csvRecords = list(csv.DictReader(StringIO(request.FILES["loadFile"].read())))
                csvRecords.sort(key=lambda x: x["name"])
                
                settings = self.createChangedItemsList(csvRecords)

                form.is_bound = False  # reset the flag so we can add new data
                form.fields["updates"].initial = json.dumps(settings) # stash the update values in the form
                self.context["settings"] = settings
                self.context["upload"] = False
                self.context["form"] = form
                self.context["submit"] = "Update Settings"
                return render(request, "dbkeeper/load_settings.html", self.context)
            else:
                # Form did not validate, try again
                self.context["form"] = form
                self.context["upload"] = True
                return render(request, "dbkeeper/load_settings.html", self.context)
        else:
            # Retrieve the changed items list and the checkboxes, and update the table
            form = LoadSettingsForm(request.POST)
            if form.is_valid():
                settings = json.loads(form.cleaned_data["updates"]) # retrieve stashed update values
                for s in settings:
                    # Update the table based on the checkboxes
                    if s["name"] in request.POST and request.POST[s["name"]] == u"on":
                        try:
                            setting = Setting.objects.get(name=s["name"])
                            setting.value = s["value"]
                            setting.description = s["description"]
                        except Setting.DoesNotExist:
                            setting = Setting(name=s["name"], value=s["value"], description=s["description"])
                        setting.save()
            
                return HttpResponseRedirect("/admin/dbkeeper/setting/")
            else:
                # Form did not validate, don't know what went wrong
                return Http404()

    def createChangedItemsList(self, csvRecords):
        # Get the existing settings from the table
        qs = Setting.objects.all()
        values = dict(zip([x.name for x in qs],
                          [{"name": x.name,
                            "value": x.value,
                            "description": x.description,
                            "disp": "update",
                           } for x in qs])) # values indexed by name
        settings = [] # record new variables or existing with updated values
        for r in csvRecords:
            if r["name"] not in values:
                settings.append({"name": r["name"],
                                 "value": r["value"].strip(),
                                 "description": r["description"].strip(),
                                 "disp": "new",
                                })

            elif r["value"].strip() != values[r["name"]]["value"].strip() or \
                 r["description"].strip() != values[r["name"]]["description"].strip():
                settings.append({"name": r["name"],
                                 "value": r["value"].strip(),
                                 "description": r["description"].strip(),
                                 "disp": "update",
                                })
        return settings
        
#----------------------------------------------------------------------------
class CompetitionStart(View):
    context = {
               "form":   None,
               "entity": "Competition Start",
               "submit": "Let the Games Begin!",
              }

    @method_decorator(login_required)
    def get(self, request):
        """ Display the form """
        self.context["form"] = CompetitionStartForm()
        return render(request, "dbkeeper/competition_start.html", self.context)
    
    @method_decorator(login_required)
    def post(self, request):
        form = CompetitionStartForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["deleteEvents"]:
                # Warning:  this will delete all PiEvents, AND
                # will also delete anything linked to one of these
                # records through a foreign key unless they have
                # on_delete=SET_NULL or something similar
                querySet = PiEvent.objects.all()
                
                if form.cleaned_data["preserveStationJoins"]:
                    querySet = querySet.exclude(type=PiEvent.JOIN_MSG_TYPE).exclude(type=PiEvent.LEAVE_MSG_TYPE)
                if form.cleaned_data["preserveTeamRegistrations"]: 
                    querySet = querySet.exclude(type=PiEvent.REGISTER_MSG_TYPE).exclude(type=PiEvent.UNREGISTER_MSG_TYPE)
                if form.cleaned_data["preserveStationStatus"]: 
                    querySet = querySet.exclude(type=PiEvent.STATION_STATUS_MSG_TYPE)
                    
                # Do the delete
                querySet.delete()
                
            PiEvent.addEvent(type=PiEvent.EVENT_STARTED_MSG_TYPE,
                             status=PiEvent.INFO_STATUS,
                             message="Start of Competition")
            
            return HttpResponseRedirect("/dbkeeper/")
        
        self.context["form"] = form
        return render(request, "dbkeeper/competition_start.html", self.context)

#----------------------------------------------------------------------------
class CompetitionEnd(View):
    context = {
               "form":   None,
               "entity": "Competition End",
               "submit": "The Games are Concluded!",
              }

    @method_decorator(login_required)
    def get(self, request):
        """ Display the form """
        self.context["form"] = CompetitionEndForm()
        return render(request, "dbkeeper/competition_end.html", self.context)
    
    @method_decorator(login_required)
    def post(self, request):
        form = CompetitionEndForm(request.POST)
        if form.is_valid():
            PiEvent.addEvent(type=PiEvent.EVENT_CONCLUDED_MSG_TYPE,
                             status=PiEvent.INFO_STATUS,
                             message="End of Competition")
            return HttpResponseRedirect("/dbkeeper/")
        
        self.context["form"] = form
        return render(request, "dbkeeper/competition_end.html", self.context)
        
#----------------------------------------------------------------------------
class LogMessage(View):
    context = {
               "form":   None,
               "entity": "Insert Log Message Event",
               "submit": "Insert Message",
              }

    @method_decorator(login_required)
    def get(self, request):
        """ Display the form """
        self.context["form"] = LogMessageForm()
        return render(request, "dbkeeper/log_msg.html", self.context)
    
    @method_decorator(login_required)
    def post(self, request):
        form = LogMessageForm(request.POST)
        if form.is_valid():
            PiEvent.addEvent(type=PiEvent.LOG_MESSAGE_MSG_TYPE,
                             status=PiEvent.INFO_STATUS,
                             message=form.cleaned_data["messageText"])
            return HttpResponseRedirect("/dbkeeper/")
        
        self.context["form"] = form
        return render(request, "dbkeeper/log_msg.html", self.context)

            

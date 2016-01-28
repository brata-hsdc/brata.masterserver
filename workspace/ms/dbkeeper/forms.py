"""ms.dbkeeper Form definitions """
from django import forms

from .models import Organization, Team
from .team_code import TeamPassCode

#----------------------------------------------------------------------------
class AddOrganizationForm(forms.Form):
    name = forms.CharField(label="Organization Name")
    type = forms.ChoiceField(label="Organization Type", choices=Organization.TYPE_CHOICES, initial=Organization.UNKNOWN_TYPE, required=False)

#----------------------------------------------------------------------------
class AddUserForm(forms.Form):
    username     = forms.CharField(label="User Name")
    password     = forms.CharField(label="Password")
    firstName    = forms.CharField(label="First Name", required=False)
    lastName     = forms.CharField(label="Last Name")
    email        = forms.CharField(label="Email Address", required=False)
    organization = forms.ModelChoiceField(label="Organization", queryset=Organization.objects.all().order_by("name"), required=True)
    mobilePhone  = forms.CharField(label="Mobile Phone", required=False)
    workPhone    = forms.CharField(label="Work Phone", required=False)
    otherPhone   = forms.CharField(label="Other Phone", required=False)
    note         = forms.CharField(label="Note", widget=forms.Textarea, required=False)

#----------------------------------------------------------------------------
class AddTeamForm(forms.Form):
    name = forms.CharField(label="Team Name")
    organization = forms.ModelChoiceField(label="School", queryset=Organization.objects.filter(type=Organization.SCHOOL_TYPE).order_by("name"))

#----------------------------------------------------------------------------
class CheckInTeamForm(forms.Form):
    team = forms.ModelChoiceField(label="Team Name", queryset=Team.objects.all().order_by("name"))
#     school = forms.ModelChoiceField(label="School", queryset=Organization.objects.filter(type=Organization.SCHOOL_TYPE).order_by("name"))
    teamCode1 = forms.ChoiceField(label="Team Code", choices=[(b,a) for a,b in TeamPassCode.LETTER_LIST], required=False)
    teamCode2 = forms.ChoiceField(label="", choices=[(b,a) for a,b in TeamPassCode.LETTER_LIST], required=False)
    teamCode3 = forms.ChoiceField(label="", choices=[(b,a) for a,b in TeamPassCode.LETTER_LIST], required=False)
    teamCode4 = forms.ChoiceField(label="", choices=[(b,a) for a,b in TeamPassCode.NUMBER_LIST], required=False)
#     teamCode = forms.CharField(label="Code", required=False)

#----------------------------------------------------------------------------
class AddLaunchParamsForm(forms.Form):
    pass

#----------------------------------------------------------------------------
class AddDockParamsForm(forms.Form):
    # TODO:  How many tapes will we have?
    tapeLen1 = forms.FloatField(label="Tape 1 Length (m)", initial="0.0", required=False)
    tapeLen2 = forms.FloatField(label="Tape 2 Length (m)", initial="0.0", required=False)
    tapeLen3 = forms.FloatField(label="Tape 3 Length (m)", initial="0.0", required=False)
    tapeLen4 = forms.FloatField(label="Tape 4 Length (m)", initial="0.0", required=False)
    tapeLen5 = forms.FloatField(label="Tape 5 Length (m)", initial="0.0", required=False)
    tapeLen6 = forms.FloatField(label="Tape 6 Length (m)", initial="0.0", required=False)
    
    aftAccel     = forms.FloatField(label="Aft (rear) engine acceleration (m/s^2)", initial="0.15")
    foreAccel    = forms.FloatField(label="Fore (front) engine acceleration (m/s^2)", initial="0.09")
    fuelRate     = forms.FloatField(label="Fuel consumption rate (kg/s)", initial="0.7")
    fuelQuantity = forms.FloatField(label="Fuel quantity (kg)", initial="20.0")
    minDockVel   = forms.FloatField(label="Min dock velocity (m/s)", initial="0.01")
    maxDockVel   = forms.FloatField(label="Max dock velocity (m/s)", initial="0.1")
    initialVel   = forms.FloatField(label="Initial velocity (m/s)", initial="0.0")
    simTime      = forms.IntegerField(label="Simulation run time (s)", initial="45")

#----------------------------------------------------------------------------
class AddSecureParamsForm(forms.Form):
    pass

#----------------------------------------------------------------------------
class AddReturnParamsForm(forms.Form):
    pass

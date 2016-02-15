"""ms.dbkeeper Form definitions """
from django import forms

import operator

from .models import Organization, Team
from .team_code import TeamPassCode
from piservice.models import PiEvent, PiStation

#----------------------------------------------------------------------------
class FilteredFileField(forms.FileField):
    """ A file input field for uploading files, that filters on extension """
    widget = None
    attrs = {}
    def __init__(self, *args, **kwargs):
        self.attrs = kwargs.pop("attrs", {})
        self.attrs["accept"] = kwargs.pop("accept", None)
        self.widget = forms.ClearableFileInput(attrs=self.attrs)
        super(FilteredFileField, self).__init__(*args, **kwargs)

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
    rv0lat   = forms.CharField(label="Lat")
    rv0lon   = forms.CharField(label="Lon")
    rv0angle = forms.CharField(label="Angle")
    rv0name  = forms.CharField(label="Name", initial="red_v1")
    
    rv1lat   = forms.CharField(label="Lat")
    rv1lon   = forms.CharField(label="Lon")
    rv1angle = forms.CharField(label="Angle")
    rv1name  = forms.CharField(label="Name", initial="red_v2")

    rv2lat   = forms.CharField(label="Lat")
    rv2lon   = forms.CharField(label="Lon")
    rv2angle = forms.CharField(label="Angle")
    rv2name  = forms.CharField(label="Name", initial="red_v3")

    rvcname  = forms.CharField(label="Center Name", initial="red_c")
    rsidelen = forms.CharField(label="Side Length")

    gv0lat   = forms.CharField(label="Lat")
    gv0lon   = forms.CharField(label="Lon")
    gv0angle = forms.CharField(label="Angle")
    gv0name  = forms.CharField(label="Name", initial="green_v1")
    
    gv1lat   = forms.CharField(label="Lat")
    gv1lon   = forms.CharField(label="Lon")
    gv1angle = forms.CharField(label="Angle")
    gv1name  = forms.CharField(label="Name", initial="green_v2")

    gv2lat   = forms.CharField(label="Lat")
    gv2lon   = forms.CharField(label="Lon")
    gv2angle = forms.CharField(label="Angle")
    gv2name  = forms.CharField(label="Name", initial="green_v3")

    gvcname  = forms.CharField(label="Center Name", initial="green_c")
    gsidelen = forms.CharField(label="Side Length")

    bv0lat   = forms.CharField(label="Lat")
    bv0lon   = forms.CharField(label="Lon")
    bv0angle = forms.CharField(label="Angle")
    bv0name  = forms.CharField(label="Name", initial="blue_v1")
    
    bv1lat   = forms.CharField(label="Lat")
    bv1lon   = forms.CharField(label="Lon")
    bv1angle = forms.CharField(label="Angle")
    bv1name  = forms.CharField(label="Name", initial="blue_v2")

    bv2lat   = forms.CharField(label="Lat")
    bv2lon   = forms.CharField(label="Lon")
    bv2angle = forms.CharField(label="Angle")
    bv2name  = forms.CharField(label="Name", initial="blue_v3")

    bvcname  = forms.CharField(label="Center Name", initial="blue_c")
    bsidelen = forms.CharField(label="Side Length")

#----------------------------------------------------------------------------
class AddDockParamsForm(forms.Form):
    """ This is a dynamic form so it is structured differently from the
        static forms.
    """
    def __init__(self, *args, **kwargs):
        super(AddDockParamsForm, self).__init__(*args, **kwargs)
        #self.setFixedFields()
        
    def setFixedFields(self):
        self.fields["minDockVel"]  = forms.FloatField(label="Min dock velocity (m/s)", initial="0.01")
        self.fields["maxDockVel"]  = forms.FloatField(label="Max dock velocity (m/s)", initial="0.1")
        self.fields["initDockVel"] = forms.FloatField(label="Initial velocity (m/s)", initial="0.0")
        self.fields["simTime"]     = forms.IntegerField(label="Simulation run time (s)", initial="45")
        
        self.fields["numRows"] = forms.IntegerField(label="Number of tapes", initial=0, widget=forms.HiddenInput())
        
    def setFields(self, numRows=0):
        for n in range(0, numRows):
            ns = str(n)
            self.fields["tapeId_" + ns]       = forms.IntegerField(label="Tape ID", required=False)
            self.fields["tapeLen_" + ns]      = forms.FloatField(label="Tape Length (m)", required=False)
            self.fields["aftAccel_" + ns]     = forms.FloatField(label="Aft (rear) engine acceleration (m/s^2)", required=False)
            self.fields["foreAccel_" + ns]    = forms.FloatField(label="Fore (front) engine acceleration (m/s^2)", required=False)
            self.fields["fuelRate_" + ns]     = forms.FloatField(label="Fuel consumption rate (kg/s)", required=False)
            self.fields["fuelQuantity_" + ns] = forms.FloatField(label="Fuel quantity (kg)", required=False)
        
    def setData(self, dockParams):
        """ Add the data values that will be used to initialize the form fields """
        self.data["numRows"]     = len(dockParams["sets"])
        self.data["minDockVel"]  = dockParams["min_dock"]
        self.data["maxDockVel"]  = dockParams["max_dock"]
        self.data["initDockVel"] = dockParams["init_vel"]
        self.data["simTime"]     = dockParams["sim_time"]
        
        for n,s in enumerate(dockParams["sets"]):
            ns = str(n)
            self.data["tapeId_" + ns]       = s["tape_id"]
            self.data["tapeLen_" + ns]      = s["tape_len"]
            self.data["aftAccel_" + ns]     = s["a_aft"]
            self.data["foreAccel_" + ns]    = s["a_fore"]
            self.data["fuelRate_" + ns]     = s["f_rate"]
            self.data["fuelQuantity_" + ns] = s["f_qty"]

        self.data["sets"] = dockParams["sets"]

        self.is_bound = True
        return self.data

    def validate(self, post):
        """ Validate the contents of the form """
        for name,field in self.fields.items():
            try:
                if name in post:
                    field.clean(post[name])
            except forms.ValidationError, e:
                self.errors[name] = e.messages    
    
    def buildStructure(self, data):
        """ Put the data fields into the structure specified in models.getDockParams() """
        s = { "min_dock": float(data["minDockVel"]),
              "max_dock": float(data["maxDockVel"]),
              "init_vel": float(data["initDockVel"]),
              "sim_time": int(data["simTime"]),
              "sets": [],
            }
        
        n = 0
        nRows = int(data["numRows"])
        while len(s["sets"]) < nRows and n < 100: # stop searching for more than 100 rows
            if "tapeId_{}".format(n) in data:
                set = { "tape_id":  data["tapeId_{}".format(n)],
                        "tape_len": data["tapeLen_{}".format(n)],
                        "a_aft":    data["aftAccel_{}".format(n)],
                        "a_fore":   data["foreAccel_{}".format(n)],
                        "f_rate":   data["fuelRate_{}".format(n)],
                        "f_qty":    data["fuelQuantity_{}".format(n)],
                      }
                # If all the values in the set are None, row was deleted from form
                if not self.listIsAllNone(set.values()):
                    # cast values to their proper types
                    set["tape_id"]  = int(set["tape_id"])
                    set["tape_len"] = float(set["tape_len"])
                    set["a_aft"]    = float(set["a_aft"])
                    set["a_fore"]   = float(set["a_fore"])
                    set["f_rate"]   = float(set["f_rate"])
                    set["f_qty"]    = float(set["f_qty"])
                    s["sets"].append(set)
            n += 1
        return s
    
    def listIsAllNone(self, lst):
        """ Return True if every element of the list is None """
        return reduce(operator.__and__, [n is None for n in lst])
    
#----------------------------------------------------------------------------
class AddSecureParamsForm(forms.Form):
    """ This is a dynamic form so it is structured differently from the
        static forms.
    """
    def __init__(self, *args, **kwargs):
        super(AddSecureParamsForm, self).__init__(*args, **kwargs)
        #self.setFixedFields()
        
    def setFields(self, numRows=0):
        self.fields["numRows"] = forms.IntegerField(label="Number of sets", initial=0, widget=forms.HiddenInput())
        for n in range(0, numRows):
            ns = str(n)
            self.fields["f0_" + ns] = forms.IntegerField(label="Freq0", required=False)
            self.fields["f1_" + ns] = forms.IntegerField(label="Freq1", required=False)
            self.fields["f2_" + ns] = forms.IntegerField(label="Freq2", required=False)
            self.fields["f3_" + ns] = forms.IntegerField(label="Freq3", required=False)
            self.fields["f4_" + ns] = forms.IntegerField(label="Freq4", required=False)
            self.fields["f5_" + ns] = forms.IntegerField(label="Freq5", required=False)
            self.fields["f6_" + ns] = forms.IntegerField(label="Freq6", required=False)
            self.fields["f7_" + ns] = forms.IntegerField(label="Freq7", required=False)
            self.fields["f8_" + ns] = forms.IntegerField(label="Freq8", required=False)
            self.fields["v0_" + ns] = forms.IntegerField(label="Value0", required=False)
            self.fields["v1_" + ns] = forms.IntegerField(label="Value1", required=False)
            self.fields["v2_" + ns] = forms.IntegerField(label="Value2", required=False)
            self.fields["v3_" + ns] = forms.IntegerField(label="Value3", required=False)
        
    def setData(self, secureParams):
        """ Add the data values that will be used to initialize the form fields """
        self.data["numRows"] = len(secureParams)
        for n,s in enumerate(secureParams):
            ns = str(n)
            self.fields["f0_" + ns] = s["f0"]
            self.fields["f1_" + ns] = s["f1"]
            self.fields["f2_" + ns] = s["f2"]
            self.fields["f3_" + ns] = s["f3"]
            self.fields["f4_" + ns] = s["f4"]
            self.fields["f5_" + ns] = s["f5"]
            self.fields["f6_" + ns] = s["f6"]
            self.fields["f7_" + ns] = s["f7"]
            self.fields["f8_" + ns] = s["f8"]
            self.fields["v0_" + ns] = s["v0"]
            self.fields["v1_" + ns] = s["v1"]
            self.fields["v2_" + ns] = s["v2"]
            self.fields["v3_" + ns] = s["v3"]

        self.data["sets"] = secureParams

        self.is_bound = True
        return self.data

    def validate(self, post):
        """ Validate the contents of the form """
        for name,field in self.fields.items():
            try:
                if name in post:
                    field.clean(post[name])
            except forms.ValidationError, e:
                self.errors[name] = e.messages    
    
    def buildStructure(self, data):
        """ Put the data fields into the structure specified in models.getSecureParams() """
        n = 0
        nRows = int(data["numRows"])
        s = data["sets"]
        while len(s) < nRows and n < 100: # stop searching for more than 100 rows
            if "f0_{}".format(n) in data:
                grp = { "f0": data["f0_{}".format(n)],
                        "f1": data["f1_{}".format(n)],
                        "f2": data["f2_{}".format(n)],
                        "f3": data["f3_{}".format(n)],
                        "f4": data["f4_{}".format(n)],
                        "f5": data["f5_{}".format(n)],
                        "f6": data["f6_{}".format(n)],
                        "f7": data["f7_{}".format(n)],
                        "f8": data["f8_{}".format(n)],
                        "v0": data["v0_{}".format(n)],
                        "v1": data["v1_{}".format(n)],
                        "v2": data["v2_{}".format(n)],
                        "v3": data["v3_{}".format(n)],
                      }
                # If all the values in the set are None, row was deleted from form
                if not self.listIsAllNone(set.values()):
                    # cast values to their proper types
                    grp["f0"] = int(grp["f0"])
                    grp["f1"] = int(grp["f1"])
                    grp["f2"] = int(grp["f2"])
                    grp["f3"] = int(grp["f3"])
                    grp["f4"] = int(grp["f4"])
                    grp["f5"] = int(grp["f5"])
                    grp["f6"] = int(grp["f6"])
                    grp["f7"] = int(grp["f7"])
                    grp["f8"] = int(grp["f8"])
                    grp["v0"] = int(grp["v0"])
                    grp["v1"] = int(grp["v1"])
                    grp["v2"] = int(grp["v2"])
                    grp["v3"] = int(grp["v3"])
                    s["sets"].append(grp)
            n += 1
        return s
    
    def listIsAllNone(self, lst):
        """ Return True if every element of the list is None """
        return reduce(operator.__and__, [n is None for n in lst])


#----------------------------------------------------------------------------
class AddReturnParamsForm(forms.Form):
    # Station 1
    st0id = forms.CharField(initial="Station 1")
    st0v0 = forms.IntegerField(initial="0")
    st0v1 = forms.IntegerField(initial="0")
    st0v2 = forms.IntegerField(initial="0")
    st0v3 = forms.IntegerField(initial="0")
    st0v4 = forms.IntegerField(initial="0")
    st0v5 = forms.IntegerField(initial="0")
    
    # Station 2
    st1id = forms.CharField(initial="Station 2")
    st1v0 = forms.IntegerField(initial="0")
    st1v1 = forms.IntegerField(initial="0")
    st1v2 = forms.IntegerField(initial="0")
    st1v3 = forms.IntegerField(initial="0")
    st1v4 = forms.IntegerField(initial="0")
    st1v5 = forms.IntegerField(initial="0")
    
    # Station 3
    st2id = forms.CharField(initial="Station 3")
    st2v0 = forms.IntegerField(initial="0")
    st2v1 = forms.IntegerField(initial="0")
    st2v2 = forms.IntegerField(initial="0")
    st2v3 = forms.IntegerField(initial="0")
    st2v4 = forms.IntegerField(initial="0")
    st2v5 = forms.IntegerField(initial="0")
    
    # Station 4
    st3id = forms.CharField(initial="Station 4")
    st3v0 = forms.IntegerField(initial="0")
    st3v1 = forms.IntegerField(initial="0")
    st3v2 = forms.IntegerField(initial="0")
    st3v3 = forms.IntegerField(initial="0")
    st3v4 = forms.IntegerField(initial="0")
    st3v5 = forms.IntegerField(initial="0")
    
    # Station 5
    st4id = forms.CharField(initial="Station 5")
    st4v0 = forms.IntegerField(initial="0")
    st4v1 = forms.IntegerField(initial="0")
    st4v2 = forms.IntegerField(initial="0")
    st4v3 = forms.IntegerField(initial="0")
    st4v4 = forms.IntegerField(initial="0")
    st4v5 = forms.IntegerField(initial="0")
    
    # Station 6
    st5id = forms.CharField(initial="Station 6")
    st5v0 = forms.IntegerField(initial="0")
    st5v1 = forms.IntegerField(initial="0")
    st5v2 = forms.IntegerField(initial="0")
    st5v3 = forms.IntegerField(initial="0")
    st5v4 = forms.IntegerField(initial="0")
    st5v5 = forms.IntegerField(initial="0")
    
# #----------------------------------------------------------------------------
# class SaveSettingsForm(forms.Form):
#     saveFile = forms.FileField(label="Save to File", accept=".csv", max_length=250)
#     
#----------------------------------------------------------------------------
class LoadSettingsForm(forms.Form):
    loadFile = FilteredFileField(label="Load from File", accept=".csv", max_length=250, required=False)
    updates = forms.CharField(widget=forms.HiddenInput(), label="updates", max_length=1000000, required=False)

#----------------------------------------------------------------------------
class CompetitionStartForm(forms.Form):
    deleteEvents = forms.BooleanField(label="Delete All Events except those checked below", required=False, initial=False)
    preserveStationJoins = forms.BooleanField(label="Preserve Station JOIN and LEAVE Events", required=False, initial=True)
    preserveTeamRegistrations = forms.BooleanField(label="Preserve Team REGISTER and UNREGISTER Events", required=False, initial=True)
    preserveStationStatus = forms.BooleanField(label="Preserve STATION_STATUS Message Events", required=False, initial=True)

#----------------------------------------------------------------------------
class CompetitionEndForm(forms.Form):
    pass

#----------------------------------------------------------------------------
class LogMessageForm(forms.Form):
    messageText = forms.CharField(label="Message Text", widget=forms.Textarea)

#----------------------------------------------------------------------------
class DisplayEventsForm(forms.Form):
    teams      = forms.ModelMultipleChoiceField(label="Team", queryset=Team.objects.all().order_by("name"), required=False)
    challenges = forms.MultipleChoiceField(label="Challenges", required=False, choices=PiStation.STATION_TYPE_CHOICES, widget=forms.CheckboxSelectMultiple())
    eventTypes = forms.MultipleChoiceField(label="Events", choices=PiEvent.TYPE_CHOICES, required=False)

    
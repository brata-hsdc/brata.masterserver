"""ms.dbkeeper Form definitions """
from django import forms

from .models import Organization

class AddOrganizationForm(forms.Form):
    name = forms.CharField(label="Organization Name")
    type = forms.ChoiceField(label="Organization Type", choices=Organization.TYPE_CHOICES, initial=Organization.UNKNOWN_TYPE, required=False)

class AddUserForm(forms.Form):
    username     = forms.CharField(label="User Name")
    password     = forms.CharField(label="Password")
    firstName    = forms.CharField(label="First Name", required=False)
    lastName     = forms.CharField(label="Last Name")
    email        = forms.CharField(label="Email Address", required=False)
    organization = forms.ModelChoiceField(queryset=Organization.objects.all().order_by("name"), required=True)
    mobilePhone  = forms.CharField(label="Mobile Phone", required=False)
    workPhone    = forms.CharField(label="Work Phone", required=False)
    otherPhone   = forms.CharField(label="Other Phone", required=False)
    note         = forms.CharField(label="Note", widget=forms.Textarea, required=False)

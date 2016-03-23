"""ms.piservice Form definitions """
from django import forms

import operator

from .models import PiStation

#----------------------------------------------------------------------------
class AddLibraryTestForm(forms.Form):
    stations = forms.ModelMultipleChoiceField(label="Station",
                                              queryset=PiStation.objects.all().order_by("station_id"),
                                              required=True)

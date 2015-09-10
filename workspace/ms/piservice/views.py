from django.shortcuts import render, Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

import json

from .models import PiEvent
from dbkeeper.models import Team
from dbkeeper.team_code import TeamCode

# Create your views here.

def index(request):
    """ Home page view for piservice.  Since this is a service, we could
        return 404, or we could put up a helpful page with some options.
    """
    return Http404()

def register(request, brataVersion=None):
    """ Handle a registration request from a BRATA device. """
    raise ValueError
    if request.method == "POST":
        # Extract JSON msg from POST data
        # Store in database
        # Return a welcome msg formatted as JSON
        return HttpResponse()
    else:
        # Return some other response
        return Http404()

#----------------------------------------------------------------------------
# Tests:
#
#   Request                                  |  Response
#   -----------------------------------------|----------
#   http://ms/piservice/                     |  404
#   http://ms/piservice/index.html           |  404
#   http://ms/piservice/register/            |  ?
#   http://ms/piservice/register/brata-v00   |  ?
#   http://ms/piservice/register/brata-v03   |  ?
#

#----------------------------------------------------------------------------
class JSONHandlerView(View):
    """ Base class for class-based views that handle JSON transactions. """
    
    def clientSpeaksJSON(self, request):
        """ Determine whether requester can send and receive JSON. """
        # Check that the client is sending JSON-formatted data
        if "application/json" in request.META["CONTENT_TYPE"]:
        
            # Check that client accepts a JSON-formatted response
            if "application/json" in request.META["HTTP_ACCEPT"]:
                return True
            
        return False
        
#----------------------------------------------------------------------------
class Register(JSONHandlerView):
    """ A class-based view to handle a BRATA Register message.
    
        The client sends a POST message with the following JSON data:
        {
            "team_id":        "<team id code>",
            "brata_version":  "nn",
            "message":        "<anything>"
        }
        The MS sends the following response on success:
        {
            "message":  "Welcome, Team '<team_name>', to the 2016 Harris High School Design Challenge!
                        You have successfully registered for the competition.  Good luck!!"
        }
    """
    
    def post(self, request, *args, **kwargs):
        """ Handle the Registration POST message and update the database """
        
        # Check that the client sends and receives JSON-formatted data
        if not self.clientSpeaksJSON(request):
            # Client doesn't accept JSON so send plain text
            PiEvent.addEvent(type=PiEvent.REGISTER_MSG_TYPE,
                             data=request.body,
                             status=PiEvent.FAIL_STATUS,
                             message="Badly formed request",
                            )
            return HttpResponse("Cannot converse in JSON", content_type="text/plain", status=400)
        
        jsonResponse = {"message": "" }
        
        # Get input parameters from URL and/or POST data
        data = json.loads(request.body)  # POST data (in JSON format)
        
        try:
            team_id       = data["team_id"]
            brata_version = data["brata_version"]
#             message       = data["message"]  # unused
        except KeyError,e:
            # Send a fail response
            PiEvent.addEvent(type=PiEvent.REGISTER_MSG_TYPE,
                             data=request.body,
                             status=PiEvent.FAIL_STATUS,
                             message="Badly formed request",
                            )
            jsonResponse["message"] = "Badly formed request: {}".format(repr(data))
            return HttpResponse(json.dumps(jsonResponse), content_type="application/json", status=400)
        
        # Retrieve the Team record using the team_code from the Register request
        # Try it as-is and decoded.
        try:
            team = Team.objects.get(code=team_id)
        except ObjectDoesNotExist:
            try:
                team = Team.objects.get(code=TeamCode.unwordify(team_id))
            except ObjectDoesNotExist:
                team = None
        
        if team is None:
            # Failed:  Record the transaction and what went wrong
            PiEvent.addEvent(type=PiEvent.REGISTER_MSG_TYPE,
                             team=team,
                             data=request.body,
                             status=PiEvent.FAIL_STATUS,
                             message="Failed to retrieve Team '{}' from the database".format(team_id),
                            )
            jsonResponse["message"] = "Invalid team_code: '{}'".format(team_id)
            return HttpResponse(json.dumps(jsonResponse), content_type="application/json", status=400)
        
        # Succeeded:  Record the transaction and update the team record
        event = PiEvent.addEvent(type=PiEvent.REGISTER_MSG_TYPE,
                                 team=team,
                                 data=request.body,
                                 status=PiEvent.SUCCESS_STATUS,
                                 message="Team '{}' sent a Register message with brata_version '{}'".format(team.name, brata_version),
                                )
        
        team.registered = event  # not checking for multiple registrations, so multiple is ok
        team.save()
        
        # Send a success response
        jsonResponse["message"] = "Welcome, Team '{}', to the 2016 Harris High School Design Challenge!  You have successfully registered for the competition.  Good luck!!".format(team.name)
        return HttpResponse(json.dumps(jsonResponse), content_type="application/json", status=200)
    
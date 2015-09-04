from django.shortcuts import render, Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.utils import timezone

import json

from .models import PiEvent
from dbkeeper.models import Team

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
    """ A class-based view to handle a BRATA Register message. """
    
    def post(self, request, *args, **kwargs):
        """ Handle the Registration POST message and update the database """
        
        # Check that the client sends and receives JSON-formatted data
        if not self.clientSpeaksJSON(request):
            return HttpResponse("Cannot converse in JSON", status=400)
        
        # Get input parameters from URL and/or POST data
        data = json.loads(request.body)  # POST data (in JSON format)
        
        try:
#             brata_version = data["brata_version"]
            team_id       = data["team_id"]
        except KeyError,e:
            # Send a fail response
            return HttpResponse("Badly formed request: {}".format(repr(data)), status=400)
        
        # Update the database
        team = Team.objects.get(team_id)
        
        event = PiEvent(time=timezone.now(),
                        type=PiEvent.REGISTER_MSG_TYPE,
                        team_id=team_id,
                        data=request.body,
                       )
        
        if team is None:
            # Failed:  Record the transaction and what went wrong
            event.status = PiEvent.FAIL_STATUS
            event.message = "Failed to retrieve Team from the database"
            event.save()
            return HttpResponse()

        # Succeeded:  Record the transaction and update the team record
        event.status = PiEvent.SUCCESS_STATUS
        event.save()
        
        team.registered = event.id  # not checking for multiple registrations, so multiple is ok
        team.save()
        
        # Send a success response
        return HttpResponse("Welcome, Team {}, to the 2016 Harris High School Design Challenge!  You have successfully registered for the competition.  Good luck!!".format(team.name))
    
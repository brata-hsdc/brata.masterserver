from django.shortcuts import render, Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

import json

from .models import PiEvent, PiStation
from dbkeeper.models import Team
from dbkeeper.team_code import TeamCode

# Create your views here.

#----------------------------------------------------------------------------
def index(request):
    """ Home page view for piservice.  Since this is a service, we could
        return 404, or we could put up a helpful page with some options.
    """
    return Http404()

#----------------------------------------------------------------------------
# Tests:
#
#   Request                                  |  Response
#   -----------------------------------------|----------
#   http://ms/piservice/                     |  404
#   http://ms/piservice/index.html           |  404
#   http://ms/piservice/register/            |  ?
#

#----------------------------------------------------------------------------
class JSONHandlerView(View):
    """ Base class for class-based views that handle JSON transactions.
    
        This class provides a base implementation of each of the 8 HTTP
        request methods:  get, post, put, patch, delete, head, options, and
        trace.
    """
    
    # HTTP methods
    GET     = 1
    POST    = 2
    PUT     = 3
    PATCH   = 4
    DELETE  = 5
    HEAD    = 6
    OPTIONS = 7
    TRACE   = 8
    
    def __init__(self, msgType=None, methods=None):
        self.type = msgType
        self._methodsSupported = list(methods) if methods else []
        self.jsonResponse = { "message": "" }
    
    def get(self, request, *args, **kwargs):
        """ Handle a GET message """
        if self.GET not in self._methodsSupported:
            # TODO:  Log a PiEvent for this?
            return HttpResponse("GET not supported for this message type", content_type="text/plain", status=400)

    def post(self, request, *args, **kwargs):
        """ Handle a POST message """
        if self.POST not in self._methodsSupported:
            # TODO:  Log a PiEvent for this?
            return HttpResponse("POST not supported for this message type", content_type="text/plain", status=400)

        # Check that the client sends and receives JSON-formatted data
        if not self.clientSpeaksJSON(request):
            # Client doesn't accept JSON so send plain text
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Badly formed request",
                         )
            return HttpResponse("Cannot converse in JSON", content_type="text/plain", status=400)
    
    def put(self, request, *args, **kwargs):
        """ Handle a PUT message """
        if self.PUT not in self._methodsSupported:
            # TODO:  Log a PiEvent for this?
            return HttpResponse("PUT not supported for this message type", content_type="text/plain", status=400)

    def patch(self, request, *args, **kwargs):
        """ Handle a PATCH message """
        if self.PATCH not in self._methodsSupported:
            # TODO:  Log a PiEvent for this?
            return HttpResponse("PATCH not supported for this message type", content_type="text/plain", status=400)

    def delete(self, request, *args, **kwargs):
        """ Handle a DELETE message """
        if self.DELETE not in self._methodsSupported:
            # TODO:  Log a PiEvent for this?
            return HttpResponse("DELETE not supported for this message type", content_type="text/plain", status=400)

    def options(self, request, *args, **kwargs):
        """ Handle a OPTIONS message """
        if self.OPTIONS not in self._methodsSupported:
            # TODO:  Log a PiEvent for this?
            return HttpResponse("OPTIONS not supported for this message type", content_type="text/plain", status=400)

    def trace(self, request, *args, **kwargs):
        """ Handle a TRACE message """
        if self.TRACE not in self._methodsSupported:
            # TODO:  Log a PiEvent for this?
            return HttpResponse("TRACE not supported for this message type", content_type="text/plain", status=400)

    def addEvent(self, **kwargs):
        """ Record a PiEvent in the database """
        return PiEvent.addEvent(type=self.type, **kwargs)
    
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
    def __init__(self):
        """ Initialize the base class with the type of message we will handle
            and the HTTP methods that we will accept.
        """
        super(Register, self).__init__(PiEvent.REGISTER_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, *args, **kwargs):
        """ Handle the Registration POST message and update the database """
        super(Register, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        data = json.loads(request.body)  # POST data (in JSON format)
        
        try:
            team_id       = data["team_id"]
            brata_version = data["brata_version"]
#             message       = data["message"]  # unused
        except KeyError,e:
            # Send a fail response
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Badly formed request",
                         )
            self.jsonResponse["message"] = "Badly formed request: {}".format(repr(data))
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
        
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
            self.addEvent(team=team,
                          data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Failed to retrieve Team '{}' from the database".format(team_id),
                         )
            self.jsonResponse["message"] = "Invalid team_code: '{}'".format(team_id)
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
        
        # Succeeded:  Record the transaction and update the team record
        event = self.addEvent(team=team,
                              data=request.body,
                              status=PiEvent.SUCCESS_STATUS,
                              message="Team '{}' sent a Register message with brata_version '{}'".format(team.name, brata_version),
                             )
        
        team.registered = event  # not checking for multiple registrations, so multiple is ok
        team.save()
        
        # Send a success response
        self.jsonResponse["message"] = "Welcome, Team '{}', to the 2016 Harris High School Design Challenge!  You have successfully registered for the competition.  Good luck!!".format(team.name)
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class Join(JSONHandlerView):
    """ A class-based view to handle an RPi Station Join message.
    
        The client sends a POST message with the following JSON data:
        {
            "station_id":        "<station id>",
        }
        
        The MS sends the following response on success:
        {
            "message":  ""
        }
    """
    def __init__(self):
        super(Join, self).__init__(PiEvent.JOIN_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, *args, **kwargs):
        """ Handle the Registration POST message and update the database """
        super(Join, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        data = json.loads(request.body)  # POST data (in JSON format)
        
        try:
            station_id = data["station_id"]
        except KeyError,e:
            # Send a fail response
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Badly formed request",
                         )
            self.jsonResponse["message"] = "Badly formed request: {}".format(repr(data))
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
        
        # Attempt to retrieve the PiStation record using the station_id
        try:
            station = PiStation.objects.get(host=station_id)
        except ObjectDoesNotExist:
            station = None
        
        if station is None:
            # Create a new PiStation record
            station = PiStation(host=station_id,
                                # TODO: add other relevant fields
                               )
            station.save()
        
        # Succeeded:  Record the transaction and update the station record
        event = self.addEvent(pi=station,
                              data=request.body,
                              status=PiEvent.SUCCESS_STATUS,
                              message="Station '{}' sent a Join message".format(station.host),
                             )
        
        station.joined = event  # not checking for multiple joins, so multiple is ok
        station.save()
        
        # Send a success response
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class Leave(JSONHandlerView):
    """ A class-based view to handle an RPi Station Leave message.
    
        The client sends a POST message with the following JSON data:
        {
            "station_id":        "<station id>",
        }
        
        The MS sends the following response on success:
        {
            "message":  ""
        }
    """
    def __init__(self):
        super(Leave, self).__init__(PiEvent.LEAVE_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, station_id=None, *args, **kwargs):
        """ Handle the Registration POST message and update the database """
        super(Leave, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        data = json.loads(request.body)  # POST data (in JSON format)
        
        if station_id is None:
            # Send a fail response
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Badly formed request (station_id missing)",
                         )
            self.jsonResponse["message"] = "Badly formed request (station_id missing): {}".format(repr(data))
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
        
        # Attempt to retrieve the PiStation record using the station_id
        try:
            station = PiStation.objects.get(id=station_id)
        except ObjectDoesNotExist:
            station = None
        
        if station is None:
            # Could not retrieve a PiStation record using station_id.
            # Send a fail response
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Unknown station '{}'.  (Bad station_id?)".format(station_id),
                         )
            self.jsonResponse["message"] = "Unknown station '{}'.  (Bad station_id?): {}".format(station_id, repr(data))
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
        
        # Succeeded:  Record the transaction and update the station record
        event = self.addEvent(pi=station,
                              data=request.body,
                              status=PiEvent.SUCCESS_STATUS,
                              message="Station '{}' sent a Leave message".format(station.host),
                             )
        
        station.joined = None  # Clear out the 'joined' field
        station.save()
        
        # Send a success response
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class StationStatus(JSONHandlerView):
    """ A class-based view to handle a Station Status Ajax request.
    
        The client sends a GET message with the following JSON data:
        {
        }
        
        The MS sends the following response on success:
        {
            "message":  ""
        }
    """
    def __init__(self):
        super(StationStatus, self).__init__(PiEvent.STATION_STATUS_MSG_TYPE, methods=[self.GET])
    
    def get(self, request, *args, **kwargs):
        """ Return the status of all the PiStations """
        super(StationStatus, self).get(request, *args, **kwargs)
        #return HttpResponse(json.dumps("stations"), content_type="application/json", status=200)
        
        stations = PiStation.objects.all()
        stationList = []
        stationTypes = dict(PiStation.STATION_TYPE_CHOICES)
        for s in stations:
            station = {"id": s.id, "host": s.host, "type": stationTypes[s.station_type], "joined": ""}
            if s.joined is not None:
                station["joined"] = str(s.joined.time).split(".")[0]
            stationList.append(station)
        return HttpResponse(json.dumps(stationList), content_type="application/json", status=200)
        

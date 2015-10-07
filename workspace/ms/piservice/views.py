from django.shortcuts import render, Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

import json

from .models import PiEvent, PiStation
from dbkeeper.models import Team
from dbkeeper.team_code import TeamPassCode

from datetime import timedelta, datetime

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
            "team_passcode":  "<passcode>",
            "brata_version":  "nn"
        }
        
        The MS sends the following response on success:
        {
            "reg_code":  "<registration_code>",
            "message":   "Welcome, Team '<team_name>', to the 2016 Harris High School Design Challenge!
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
            team_passcode = data["team_passcode"]
            brata_version = data["brata_version"]
        except KeyError,e:
            # Send a fail response
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Badly formed request",
                         )
            self.jsonResponse["message"] = "Badly formed request: {}".format(repr(data))
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)

        # Retrieve the Team record using the team_passcode from the Register request
        # Try it as-is and decoded.
        try:
            team = Team.objects.get(pass_code=team_passcode)
        except ObjectDoesNotExist:
            try:
                team = Team.objects.get(pass_code=TeamPassCode.unwordify(team_passcode))
            except ObjectDoesNotExist:
                team = None
        
        if team is None:
            # Failed:  Record the transaction and what went wrong
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Failed to retrieve Team '{}' from the database".format(team_passcode),
                         )
            self.jsonResponse["message"] = "Invalid team_passcode: '{}'".format(team_passcode)
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
        
        if team.reg_code is not None and team.reg_code != "":
            # Failed:  Record the transaction and what went wrong
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Device {} already registered to Team {}".format(team.reg_code, team.pass_code),
                         )
            self.jsonResponse["message"] = "You already have a device registered.  You must Unregister it before Registering another device.".format(team_passcode)
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
            
        # Create a unique registration code for this Team's registration
        team.reg_code = Team.generateRegCode()
        
        # Succeeded:  Record the transaction and update the team record
        event = self.addEvent(team=team,
                              data=request.body,
                              status=PiEvent.SUCCESS_STATUS,
                              message="Team '{}' Registered with brata_version '{}'. Assigned reg_code {}.".format(team.name, brata_version, team.reg_code),
                             )
        
#         self.jsonResponse["message"] = "DEBUG"
#         return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
    
        team.registered = event  # not checking for multiple registrations, so multiple is ok
        team.save()
        
        # Send a success response
        self.jsonResponse["reg_code"] = team.reg_code
        self.jsonResponse["message"] = "Welcome, Team '{}', to the 2016 Harris High School Design Challenge!  You have successfully registered for the competition.  Good luck!!".format(team.name)
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class Unregister(JSONHandlerView):
    """ A class-based view to handle a BRATA Unregister message.
    
        The client sends a POST message with the following JSON data:
        {
            "reg_code":  "<registration_code>"
        }
        
        The MS sends the following response on success:
        {
            "message":   "You have unregistered your BRATA device.  You may re-register it or register a different BRATA device."
        }
    """
    def __init__(self):
        """ Initialize the base class with the type of message we will handle
            and the HTTP methods that we will accept.
        """
        super(Unregister, self).__init__(PiEvent.UNREGISTER_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, *args, **kwargs):
        """ Handle the Registration POST message and update the database """
        super(Unregister, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        data = json.loads(request.body)  # POST data (in JSON format)
        
        try:
            reg_code = data["reg_code"]
        except KeyError,e:
            # Send a fail response
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Badly formed request",
                         )
            self.jsonResponse["message"] = "Badly formed request: {}".format(repr(data))
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)

        # Retrieve the Team record using the team_passcode from the Register request
        # Try it as-is and decoded.
        if reg_code is None or reg_code == "":
            reg_code = "INVALID REG CODE"
        try:
            team = Team.objects.get(reg_code=reg_code)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            # Failed:  Record the transaction and what went wrong
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Failed to retrieve Team from the database with reg_code {}".format(reg_code),
                         )
            self.jsonResponse["message"] = "Unable to find registered device to unregister."
            self.jsonResponse["reg_code"] = data["reg_code"]  # return the reg_code that was sent
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
        
        # Succeeded:  Record the transaction and update the team record
        event = self.addEvent(team=team,
                              data=request.body,
                              status=PiEvent.SUCCESS_STATUS,
                              message="Team '{}' Unregistered device with reg_code '{}'.".format(team.name, team.reg_code),
                             )
        
        # Erase the reg_code
        team.reg_code = ""
        
#         self.jsonResponse["message"] = "DEBUG"
#         return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
    
        team.registered = event  # store the Unregister event in the registered field
        team.save()
        
        # Send a success response
        self.jsonResponse["message"] = "You have unregistered your BRATA device.  You may re-register it or register a different BRATA device."
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class Join(JSONHandlerView):
    """ A class-based view to handle an RPi Station Join message.
    
        The client sends a POST message with the following JSON data:
        {
            "host":         "rte01", // hostname or ip address
            "station_type": "RTE"    // the type of competition station
            "serial_num":   "123456789" // the CPU serial number
            "url":          "http://rte01:8080/control"  // URL to send commands to station
        }
        
        The MS sends the following JSON response on success:
        {
            "station_id":  "42:xxxx"
        }
        
        This class uses STATION_IPS and STATION_SERIAL_NUMS to validate the sender.
    """
    def __init__(self):
        super(Join, self).__init__(PiEvent.JOIN_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, *args, **kwargs):
        """ Handle the Registration POST message and update the database """
        super(Join, self).post(request, *args, **kwargs)
        
        # Get input parameters from URL and/or POST data
        data = json.loads(request.body)  # POST data (in JSON format)
        
        # Validate the message format
        try:
            host         = data["host"]
            station_type = data["station_type"]
            serial_num   = data["serial_num"]
            url          = data["url"] if "url" in data else ""
        except KeyError:
            # Send a fail response
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Badly formed request",
                          )
            self.jsonResponse["message"] = "Badly formed request: {}".format(repr(data))
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
    
        # Validate the source of the message
        senderIP = request.META["REMOTE_ADDR"]  # IP address of sender
        if not PiStation.allowedHost(senderIP) or not PiStation.allowedSerialNum(serial_num):
            # Send a fail response
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Join request from invalid host ({}) or serial_num ({}).  See MS setting STATION_IPS and STATION_SERIAL_NUMS.".format(senderIP, serial_num),
                         )
            self.jsonResponse["message"] = "Join request from invalid host ({}) or serial_num ({})".format(senderIP, serial_num)
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
        
        # Retrieve existing PiStation record or create a new one
        try:
            station = PiStation.objects.get(serial_num=serial_num)
        except ObjectDoesNotExist:
            station = PiStation(host=senderIP, station_type=station_type, serial_num=serial_num, url=url)
            station.save()
        
        # Succeeded:  Record the transaction and update the station record
        station_id = station.setStationId()
        station.joined = self.addEvent(pi=station,
                                       data=request.body,
                                       status=PiEvent.SUCCESS_STATUS,
                                       message="Station '{}' ({}) sent a Join message".format(station.host, station.station_id),
                                       )
        station.last_activity = timezone.now()
        station.save()
        
        # Send a success response
        self.jsonResponse = {"station_id": station.station_id}
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class Heartbeat(JSONHandlerView):
    """ A class-based view to handle an RPi Station Heartbeat message.
    
        The client sends a GET message with the following JSON data:
        {
            "station_id":   "xxxxxxx", // unique station_id
        }
        
        The MS sends the following JSON response on success:
        {
            "station_id":  "xxxxxxx"
        }
    """
    def __init__(self):
        super(Heartbeat, self).__init__(PiEvent.JOIN_MSG_TYPE, methods=[self.GET])
    
    def get(self, request, *args, **kwargs):
        """ Handle the Registration GET message and update the database """
        super(Heartbeat, self).get(request, *args, **kwargs)
        
        # Get input parameters from URL and/or POST data
        data = json.loads(request.body)  # POST data (in JSON format)
        
        # Validate the source of the message
        senderIP = request.META["REMOTE_ADDR"]  # IP address of sender
        station = None
        if "station_id" in data:
            # Look for an existing PiStation record (this is a re-Join)
            station_id = data["station_id"]
            station = PiStation.validateStation(senderIP, station_id)
        if not station or not PiStation.allowedHost(senderIP):
            # Send a fail response
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Heartbeat received from invalid host: {}, station_id {}.  See MS setting STATION_IPS.".format(senderIP, station_id),
                         )
            self.jsonResponse["message"] = "Heartbeat message from unrecognized station: {} at address {}".format(station_id, senderIP)
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
        
#         # Succeeded:  Record the transaction and update the station record
#         event = self.addEvent(pi=station,
#                               data=request.body,
#                               status=PiEvent.SUCCESS_STATUS,
#                               message="Station '{}' ({}) sent a Heartbeat message".format(station.host, station.station_id),
#                              )
        
        # Record the current time in the station record
        station.last_activity = timezone.now()
        station.save()
        
        # Send a success response
        self.jsonResponse = {"time": str(station.last_activity)} # return the time the Heartbeat was received
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
    
    def post(self, request, *args, **kwargs):
        """ Handle the Registration POST message and update the database """
        super(Leave, self).post(request, *args, **kwargs)
        
        # Get input parameters from URL and/or POST data
        data = json.loads(request.body)  # POST data (in JSON format)
        
        try:
            station_id = data["station_id"]
        except KeyError:
            # Send a fail response
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Badly formed request",
                         )
            self.jsonResponse["message"] = "Badly formed request: {}".format(repr(data))
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)

        # Validate the source of the message
        senderIP = request.META["REMOTE_ADDR"]  # IP address of sender
        station = PiStation.validateStation(senderIP, station_id)

        if station is None:
            # Could not retrieve a PiStation record using station_id.
            # Send a fail response
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Could not find a valid station: {}".format(station_id),
                         )
            self.jsonResponse["message"] = "Could not find a valid station: {}".format(station_id, repr(data))
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
        self.jsonResponse["message"] = "Station {} has left".format(station_id)
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class StationStatus(JSONHandlerView):
    """ A class-based view to handle a Station Status Ajax request.
    
        The client sends a GET message with the following JSON data:
        {
        }
        
        The MS sends the following response on success:
        [
            {
                "host": "Second RPi Station",
                "station_id": "2:ab45",
                "joined": "2015-09-17 03:36:58",
                "type": "Unknown"
            },
            {
                "host": "First RPi Station",
                "station_id": "1:03cc",
                "joined": "",
                "type": "Unknown"
            }
        ]
    """
    def __init__(self):
        super(StationStatus, self).__init__(PiEvent.STATION_STATUS_MSG_TYPE, methods=[self.GET])
    
    def get(self, request, *args, **kwargs):
        """ Return the status of all the PiStations """
        super(StationStatus, self).get(request, *args, **kwargs)
        
        stations = PiStation.objects.all()
        stationList = []
        stationTypes = dict(PiStation.STATION_TYPE_CHOICES)
        for s in stations:
            station = {"station_id": s.station_id, 
                       "host": s.host,
                       "type": stationTypes.get(s.station_type, "Unknown"),
                       "joined": "",
                       "last_active": "",
                      }
            if s.joined is not None:
                sec = int((timezone.now() - s.joined.time).total_seconds())
                station["joined"] = self.formatSeconds(sec)
            try:
#                 latest = PiEvent.objects.filter(pi=s).latest("time").time
                latest = s.last_activity
                station["last_active"] = self.formatSeconds(int((timezone.now() - latest).total_seconds()))
            except ObjectDoesNotExist:
                pass
            stationList.append(station)
        return HttpResponse(json.dumps(stationList), content_type="application/json", status=200)
    
    def formatSeconds(self, seconds):
        """ Convert seconds to hh:mm:ss
        
            Args:
                seconds (int): number of seconds
            Returns:
                string containing hh:mm:ss
        """
        return "{:02d}:{:02d}:{:02d}".format(int(seconds/3600),int((seconds%3600)/60), seconds%60)
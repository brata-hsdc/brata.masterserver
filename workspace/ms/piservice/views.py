from django.shortcuts import render, Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

import json

from .models import PiEvent, PiStation
from dbkeeper.models import Team
from dbkeeper.team_code import TeamPassCode

from datetime import timedelta, datetime

import requests

# The following is a hack to keep our cipher from accidentally being checked in
import os
import sys
sys.path.append(os.path.abspath("/opt/designchallenge2016"))
from NoCMConfigValues import *

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
    
    class Namespace:
        """ A class just to hold attributes that can be accessed using "." notation """
        pass
    
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
            return True
            # This extra checek is failing and don't know why removing for now
            # Check that client accepts a JSON-formatted response
            #if "application/json" in request.META["HTTP_ACCEPT"]:
            #    return True
            
        return False
    
    def validateJSONFields(self, request, fields):
        """ Check the POST data for the existence of fields.
        
            A field can be mandatory or optional.  A mandatory field is
            just a string.  An optional field is a 1- or 2-tuple (or 1- or 2-list)
            containing the field name and the default value.  If no default value
            is provided, the optional value is not returned in the dict.
            
            Example:
                m = self.validateJSONFields(("field1", "field2", ("optional1", "default"),
                                             ("optional2_no_default",)))
                
                would return (if the message contained just field1 and field2):
                {
                  field1:  "value1",
                  field2:  "value2",
                  optional1:  "default"
                }
                
                and would be accessible as m.field1, m.field2, and m.optional1.
        
            Returns:
                A tuple containing (Namespace, HttpResponse) where one of the two
                elements will be None.
        """
        try:
            msgFields = self.Namespace()
            data = json.loads(request.body)  # POST data (in JSON format)
            lastError = "none"
            for f in fields:
                if isinstance(f, (str, unicode)):
                    # Mandatory field
                    if f not in data:
                        lastError = f + " not found"
                        raise
                    setattr(msgFields, f, data[f])
                else:
                    # Optional field
                    if f[0] not in data:
                        if len(f) > 1:
                            setattr(msgFields, f[0], f[1])  # store default value
                    else:
                        setattr(msgFields, f[0], data[f[0]])
            return (msgFields, None)
        except:
            # Log the message
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Badly formed JSON " + lastError,
                         )
            # Send a fail response
            self.jsonResponse["message"] = "Badly formed request: {}".format(repr(data))
            resp = HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
            return (None, resp)
    
    def validateTeam(self, request, teamCode, failureMsg):
        """ Use teamCode to retrieve a Team record.
        
            Returns:
                A tuple containing (team record, HttpResponse) where one of the two
                elements will be None.
        """
        msg2015 = self.type in PiEvent.MSG_TYPES_2015
        try:
            if msg2015:
                team = Team.objects.get(pass_code=teamCode)
            else:
                team = Team.objects.get(reg_code=teamCode)
        except ObjectDoesNotExist:
            team = None
        
        resp = None
        if team is None:
            # Failed:  Record the transaction and what went wrong
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Invalid {} {}".format("team_id" if msg2015 else "reg_code", teamCode),
                         )
            self.jsonResponse["message"] = failureMsg
            resp = HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
        return (team, resp)
            
#----------------------------------------------------------------------------
class Register(JSONHandlerView):
    """ A class-based view to handle a BRATA Register message.
    
        The client sends a POST message with the following JSON data:
        {
            "message":  "",
            "reg_code":  "may have data from a previoius registration"
        }
        and the ned of the url is the team_passcode
        
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
    
    def post(self, request, team_passcode, *args, **kwargs):
        """ Handle the Registration POST message and update the database """
        super(Register, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
#         data = json.loads(request.body)  # POST data (in JSON format)

        #m,response = self.validateJSONFields(request, (("brata_version")))
        #if m is None:
        #    return response
        
#         try:
#             team_passcode = data["team_passcode"]
#             brata_version = data["brata_version"]
#         except KeyError,e:
#             # Send a fail response
#             self.addEvent(data=request.body,
#                           status=PiEvent.FAIL_STATUS,
#                           message="Badly formed request",
#                          )
#             self.jsonResponse["message"] = "Badly formed request: {}".format(repr(data))
#             return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)

        # Retrieve the Team record using the team_passcode from the Register request
        # Try it as-is and decoded.
        # TODO: refactor this to use self.validateTeam()
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
        # We are allowing resgistration but it now generates a new code for the new registration 
        # to ensure the team is only using one device at a time
        #if team.reg_code is not None and team.reg_code != "":
        #    # Failed:  Record the transaction and what went wrong
        #    self.addEvent(data=request.body,
        #                  status=PiEvent.FAIL_STATUS,
        #                  message="Device {} already registered to Team {}".format(team.reg_code, team.pass_code),
        #                 )
        #    self.jsonResponse["message"] = "You already have a device registered.  You must Unregister it before Registering another device.".format(team_passcode)
        #    return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
            
        # Create a unique registration code for this Team's registration
        team.reg_code = Team.generateRegCode()
        
        # Succeeded:  Record the transaction and update the team record
        event = self.addEvent(team=team,
                              data=request.body,
                              status=PiEvent.SUCCESS_STATUS,
                              message="Team '{}' Registered with brata_version '{}'. Assigned reg_code {}.".format(team.name, "m.brata_version", team.reg_code),
                             )
        
#         self.jsonResponse["message"] = "DEBUG"
#         return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
    
        team.registered = event  # not checking for multiple registrations, so multiple is ok
        team.save()
        
        # Send a success response
        self.jsonResponse["reg_code"] = team.reg_code
        message = "Welcome, Team '{}', to the 2016 Harris High School Design Challenge!  You have successfully registered for the competition.  Good luck!!".format(team.name)
        self.jsonResponse["message"] = cipher(message)
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
            "station_id":         "rte01", // hostname or ip address
            "station_type": "RTE"    // the type of competition station
            "station_serial":   "123456789" // the CPU serial number
            "station_url":          "http://rte01:8080/control"  // URL to send commands to station
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
            host         = data["station_id"]
            station_type = data["station_type"]
            serial_num   = data["station_serial"]
            url          = data["station_url"] if "station_url" in data else ""
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
class AtWaypoint(JSONHandlerView):
    """ A class-based view to handle a BRATA AtWaypoint message.
    
        The client sends a POST message with the following JSON data:
        {
            "reg_code":        "<active reg_code>",
        }
        
        The MS sends the following response on success:
        {
            "message":  "You have ..."
        }
    """
    def __init__(self):
        super(AtWaypoint, self).__init__(PiEvent.AT_WAYPOINT_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, lat, lon, *args, **kwargs):
        """ Handle the POST message and update the database """
        super(AtWaypoint, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        m,response = self.validateJSONFields(request, ("reg_code",))
        if m is None:
            return response
        
        # TODO:  Add message processing
        
        # Succeeded:  Record the transaction and update the station record
        event = self.addEvent(data=request.body,
                              status=PiEvent.SUCCESS_STATUS,
                              message="AtWaypoint ({}, {}) msg received from {}".format(lat, lon, m.reg_code),
                             )
        
        # Send a success response
        self.jsonResponse["message"] = "You have successfully navigated to ...."
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class StartChallenge(JSONHandlerView):
    """ A class-based view to handle a BRATA StartChallenge message.
    
        The client sends a POST message with the following JSON data:
        {
            "reg_code":        "current reg_code",
        }
        
        The MS sends the following response on success:
        {
            "message":  "..."
        }
    """
    def __init__(self):
        super(StartChallenge, self).__init__(PiEvent.START_CHALLENGE_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, station_id, *args, **kwargs):
        """ Handle the POST message and update the database """
        super(StartChallenge, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        m,response = self.validateJSONFields(request, ("reg_code",))
        if m is None:
            return response
        
        # TODO:  Add message processing
        
        # Succeeded:  Record the transaction and update the station record
        event = self.addEvent(data=request.body,
                              status=PiEvent.SUCCESS_STATUS,
                              message="StartChallenge msg received from {}".format(m.reg_code),
                             )
        
        # Send a success response
        self.jsonResponse["message"] = "You have successfully started ...."
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class Dock(JSONHandlerView):
    """ A class-based view to handle a BRATA Dock message.
    
        The client sends a POST message with the following JSON data:
        {
            "reg_code":        "current reg_code",
            "message":         "see ICD"
        }
        
        The MS sends the following response on success:
        {
            "message":  "..."
        }
    """
    def __init__(self):
        super(Dock, self).__init__(PiEvent.DOCK_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, station_id, *args, **kwargs):
        """ Handle the POST message and update the database """
        super(Dock, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        m,response = self.validateJSONFields(request, ("reg_code","message",))
        if m is None:
            return response
        
        # TODO:  Add message processing
        
        # Succeeded:  Record the transaction and update the station record
        event = self.addEvent(data=request.body,
                              status=PiEvent.SUCCESS_STATUS,
                              message="Dock msg received from {}".format(m.reg_code),
                             )
        
        message = "Docking Parameters received!"

	# Send message to the Pi this team is registered with to start the simulation
        url = "http://192.168.4.39:5000/rpi/start_challenge"
        headers = { "Content-type": "application/json", "Accept": "application.json" }
        data = json.dumps({
                 "t_aft": "8.2",
                 "t_coast": "1",
                 "t_fore": "13.1",
                 "a_aft": "0.15",
                 "a_fore": "0.09",
                 "r_fuel": "0.7",
                 "q_fuel": "20",
                 "dist": "15.0",
                 "v_min": "0.01",
                 "v_max": "0.1",
                 "v_init": "0.0",
                 "t_sim": "45",
               })
	response = requests.post(url, data=data, headers=headers)
        if response.status_code != 200:
            message = "Could not contact simulation server.  Contact a competition official."	
            
        # Send a success response
        self.jsonResponse["message"] = message

        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class Submit(JSONHandlerView):
    """ A class-based view to handle a BRATA Submit message.
    
        The client sends a POST message with the following JSON data:
        {
            "reg_code":        "current reg_code",
        }
        
        The MS sends the following response on success:
        {
            "message":  "..."
        }
    """
    def __init__(self):
        super(Submit, self).__init__(PiEvent.SUBMIT_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, station_id, *args, **kwargs):
        """ Handle the POST message and update the database """
        super(Submit, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        m,response = self.validateJSONFields(request, ("reg_code",))
        if m is None:
            return response
        
        # TODO:  Add message processing
        
        # Succeeded:  Record the transaction and update the station record
        event = self.addEvent(data=request.body,
                              status=PiEvent.SUCCESS_STATUS,
                              message="Submit msg received from {}".format(m.reg_code),
                             )
        # Figure out if the attempt was successful
	# TODO
	wasDocked = True
        message = "Docking latches engaged! Continue to next Challenge!"
	if not wasDocked:
	    message = "TODO some error message"
	# Send a success response
        self.jsonResponse["message"] = "Docking latches engaged! Continue to next Challenge!"
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

#----------------------------------------------------------------------------
class Register_2015(JSONHandlerView):
    """ A class-based view to handle a 2015 BRATA Register message.
    
        The client sends a POST message with the following JSON data:
        {
            "team_id":        "<team ID>",
        }
        
        The MS sends the following response on success:
        {
            "message":  "..."
        }
    """
    def __init__(self):
        super(Register_2015, self).__init__(PiEvent.REGISTER_2015_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, *args, **kwargs):
        """ Handle the POST message and update the database """
        super(Register_2015, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        m,response = self.validateJSONFields(request, ("team_id",))
        if m is None:
            return response
        
        try:
            team = Team.objects.get(pass_code=m.team_id)
        except ObjectDoesNotExist:
            team = None
        if team is None:
            # Failed:  Record the transaction and what went wrong
            self.addEvent(data=request.body,
                          status=PiEvent.FAIL_STATUS,
                          message="Invalid team_id {}".format(m.team_id),
                         )
            self.jsonResponse["message"] = "You have tried to Register your BRATA device with an invalid team_id: {}".format(m.team_id)
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
            
        # Create a unique registration code for this Team's registration
        team.reg_code = Team.generateRegCode()
        
        # Succeeded:  Record the transaction and update the team record
        event = self.addEvent(team=team,
                              data=request.body,
                              status=PiEvent.SUCCESS_STATUS,
                              message="Team '{}' Registered with brata_version 'v00'. Assigned reg_code {} (not used).".format(team.name, team.reg_code),
                             )
        
        team.registered = event  # not checking for multiple registrations, so multiple is ok
        team.save()
        
        # Send a success response
        self.jsonResponse["message"] = "Welcome, Team '{}', to the 2016 Harris High School Design Challenge!  You have successfully registered for the competition.  Good luck!!".format(team.name)
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class AtWaypoint_2015(JSONHandlerView):
    """ A class-based view to handle a BRATA AtWaypoint message.
    
        The client sends a POST message with the following JSON data:
        {
            "team_id":        "<team_id>",
        }
        
        The MS sends the following response on success:
        {
            "message":  "You have ..."
        }
    """
    def __init__(self):
        super(AtWaypoint_2015, self).__init__(PiEvent.AT_WAYPOINT_2015_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, waypointId, *args, **kwargs):
        """ Handle the POST message and update the database """
        super(AtWaypoint_2015, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        m,response = self.validateJSONFields(request, ("team_id",))
        if m is None:
            return response
        
        team,response = self.validateTeam(request, m.team_id, "Received an invalid team_id: '{}'.  You may need to re-register.".format(m.team_id))
        
        # TODO:  Add message processing
        
        # Succeeded:  Record the transaction and update the station record
        event = self.addEvent(data=request.body,
                              status=PiEvent.SUCCESS_STATUS,
                              message="AtWaypoint '{}' msg received from team {}".format(waypointId, m.team_id),
                             )
        
        # Send a success response
        self.jsonResponse["message"] = "You have successfully navigated to waypoint {}".format(waypointId)
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class StartChallenge_2015(JSONHandlerView):
    """ A class-based view to handle a BRATA StartChallenge message.
    
        The client sends a POST message with the following JSON data:
        {
            "team_id":        "<team_id>",
        }
        
        The MS sends the following response on success:
        {
            "message":  "..."
        }
    """
    def __init__(self):
        super(StartChallenge_2015, self).__init__(PiEvent.START_CHALLENGE_2015_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, station_id, *args, **kwargs):
        """ Handle the POST message and update the database """
        super(StartChallenge_2015, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        m,response = self.validateJSONFields(request, ("team_id",))
        if m is None:
            return response
        
        team,response = self.validateTeam(request, m.team_id, "Received an invalid team_id: '{}'.  You may need to re-register.".format(m.team_id))
        
        # TODO:  Add message processing
        
        # Succeeded:  Record the transaction and update the station record
        event = self.addEvent(data=request.body,
                              status=PiEvent.SUCCESS_STATUS,
                              message="StartChallenge msg received from team {} at station {}".format(m.team_id, station_id),
                             )
        
        # Send a success response
        self.jsonResponse["message"] = "You are starting the challenge at station {}".format(station_id)
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class Submit_2015(JSONHandlerView):
    """ A class-based view to handle a BRATA Submit message.
    
        The client sends a POST message with the following JSON data:
        {
            "team_id":        "<team_id>",
        }
        
        The MS sends the following response on success:
        {
            "message":  "..."
        }
    """
    def __init__(self):
        super(Submit_2015, self).__init__(PiEvent.SUBMIT_2015_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, station_id, *args, **kwargs):
        """ Handle the POST message and update the database """
        super(Submit_2015, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        m,response = self.validateJSONFields(request, ("team_id",))
        if m is None:
            return response
        
        team,response = self.validateTeam(request, m.team_id, "Received an invalid team_id: '{}'.  You may need to re-register.".format(m.team_id))
        
        # TODO:  Add message processing
        
        # Succeeded:  Record the transaction and update the station record
        event = self.addEvent(data=request.body,
                              team=team,
                              status=PiEvent.SUCCESS_STATUS,
                              message="Submit msg received from team {} at station {}".format(m.team_id, station_id),
                             )
        
        # Send a success response
        self.jsonResponse["message"] = "Your results for the challenge at station {} have been submitted".format(station_id)
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

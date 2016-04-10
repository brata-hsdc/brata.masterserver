from django.shortcuts import render, Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.utils import timezone
from django.utils.http import urlquote
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q

import json

from .forms import AddLibraryTestForm
from .models import PiEvent, PiStation
from dbkeeper.models import Team, Setting
from dbkeeper.team_code import TeamPassCode

from datetime import timedelta, datetime
import time

import requests

# The following is a hack to keep our cipher from accidentally being checked in
import os
import sys
sys.path.append(os.path.abspath("/opt/designchallenge2016"))
from NoCMConfigValues import *

# for regular expression matching
import re

import random
#from jpype import * 
import qrcode
import qrcode.image.svg
import io
import base64
import cStringIO

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
                          status=PiEvent.WARNING_STATUS,
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
                          status=PiEvent.WARNING_STATUS,
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
                          status=PiEvent.WARNING_STATUS,
                          message="Invalid {} {}".format("team_id" if msg2015 else "reg_code", teamCode),
                         )
            self.jsonResponse["message"] = failureMsg
            resp = HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
        return (team, resp)

    def getTeamFromRegCode(self, reg_code, body):
        # Get the team name from the reg_code
        try:
            team = Team.objects.get(reg_code=reg_code)
        except ObjectDoesNotExist:
            team = None
        
        if team is None:
            # Failed:  Record the transaction and what went wrong
            self.addEvent(data=body,
                          status=PiEvent.WARNING_STATUS,
                          message="Failed to retrieve Team using reg_code '{}' from the database".format(reg_code),
                         )
            self.jsonResponse["message"] = cipher("Could not find a valid team: {}".format(reg_code))
            return team, HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)

        return (team, None)

    def getStationFromStationId(self, station_id, body):
        # Get the station from the station_id
        station_id = station_id.lower()
        try:
            station = PiStation.objects.get(station_id=station_id)
        except ObjectDoesNotExist:
            station = None
        
        if station is None:
            # Failed:  Record the transaction and what went wrong
            self.addEvent(data=body,
                          status=PiEvent.WARNING_STATUS,
                          message="Failed to retrieve Station using station_id '{}' from the database".format(station_id),
                         )
            self.jsonResponse["message"] = cipher("Could not find a station_id: {}".format(station_id))
            return station, HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)

        return (station, None)

    def getFieldsFromBrataMessage(self, brataMessage, fields):
        """ Extract message data from a Brata message.

            Example:
                m = self.getFieldsFromBrataMessage(message, ("field-1", "field-2",))
                
                would return (if the message contained just field1 and field2):
                {
                  field1:  "value1",
                  field2:  "value2",
                }
                
                and would be accessible as m.field1, and m.field2.
                Note the illegal - has been removed from the resulting variable name.
                Case is left unchanged so if caps in you get caps out.
        
            Returns:
                A tuple containing (Namespace, HttpResponse) where one of the two
                elements will be None.
        """
        try:
            msgFields = self.Namespace()
            lastError = "none"
            message = None
            for f in fields:
                # Build regex to find [f=*] returning * as the value for f
                if isinstance(f, (str, unicode)):
                    try:
                        value = re.search("[[]"+f+"=(.+?)[]]", brataMessage).group(1)
                    except AttributeError:
                        lastError = f + " not found"
                        message="Illegal parameter: {}".format(lastError)
                        raise
                    fValid = f.replace("-","")
                    setattr(msgFields, fValid, value)
            return (msgFields, None)
        except:
            # Log the message
            if lastError == "none":
                e = sys.exc_info()
                message = "Exception: {}".format(e)

            self.addEvent(data=message,
                          status=PiEvent.WARNING_STATUS,
                          message=message,
                         )
            # Send a fail response
            #self.jsonResponse["message"] = traceback.format_exc()
            self.jsonResponse["message"] = message # TODO put back cipher(message)
            resp = HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)
            return (None, resp)

    def getStatus(self, team, station):
        # Get submits from this station for this team
        try:
            # sort by time should provide the oldest first
            # How do we know they didn't need to restart this one because of a dead phone?
            # Doesn't matter because they still only get a total of 3 chances
            submitRequests = PiEvent.objects.filter(status=PiEvent.INFO_STATUS, type=PiEvent.STATION_SUBMIT_MSG_TYPE, team=team, pi=station).order_by('time')
            if not submitRequests.exists():
                self.jsonResponse["message"] = cipher("No simulation started at this station or simulation not complete.")
                return None, None, None, None, HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)
            attemptCount = 0
            retry = True
            wasCorrect = False
            lastAnswer = 0
            lastAttemptData = ""
            for attempt in submitRequests:
                lastAttemptData = attempt.data
                submitData = json.loads(attempt.data)
                if submitData is None:
                    return response
                if submitData["is_correct"].lower()=="true":
                    retry = False
                    wasCorrect = True
                else:
                    attemptCount = attemptCount + 1
                lastAnswer = submitData["candidate_answer"]
            if attemptCount > 2:
                retry = False
            return wasCorrect, retry, lastAnswer, lastAttemptData, None
        except:
            message = "No simulation started at this station, please check your QR Code scanned."	
            #e = sys.exc_info()
            #message = "Exception: {}".format(e)
            status = PiEvent.WARNING_STATUS
            data = ""
            event = self.addEvent(team=team,
                              pi=station,
                              data=data,
                              status=status,
                              message=message,
                             )
            self.jsonResponse["message"] = cipher(message)
            return None, None, None, None, HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

    def getDateTime(self):
         return datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

#----------------------------------------------------------------------------
class LibraryTest(View):
    """ Display the QR Code test page.
    
    Lets the user first choose a station and hit submit.
    Returns a page containing QR codes specific to running the
    challenge on the chosen station.
    """
    MS_BASE_URL = "http://localhost"
    #QR_SERVICE_REQUEST_URL = "http://zxing.org/w/chart?cht=qr&chs=350x350&chld=L&choe=UTF-8&chl="
    QR_SERVICE_REQUEST_URL = Setting.get("MS_EXTERNAL_HOST_ADDRESS", default=MS_BASE_URL)+"/piservice/qrcode?chl="
    context = {
               "form": None,
               "all_stations_table":   None,
               "station_table":   None,
               "url_table":   None,
               "server_ip":   None,
               "selected_id":   None,
              }

    def get(self, request):
        """ Create and return a blank form. """
        self.context["form"] = AddLibraryTestForm()
        return render(request, "piservice/libraryTest.html", self.context)

    def post(self, request):
        """ Create QR codes that can be used to run the requested station.
        
        First, construct the URLs that the Brata will need to send to the
        MS.  Then create requests to the QR service to get the QR code
        graphic for each URL.  Then insert them into the web page template
        for display.
        """
        form = AddLibraryTestForm(request.POST)
        self.context["form"] = form
        if form.is_valid():
            stations = form.cleaned_data["stations"]

            # Get the MS server external URL
            msUrl = Setting.get("MS_EXTERNAL_HOST_ADDRESS", default=self.MS_BASE_URL) + "/piservice"
            
            # Create a table with one row of URLs for each station.
            self.context["station_table"] = []
            for station in stations:
                # Create an arrival QR code for every station_type
                stationRow = {"station_id": station.station_id,
                              "urls": [self.qr("Arrive", "start_challenge", station.station_id, msUrl)]
                             }
                
                # Create additional codes based on the station_type
                if station.station_type == PiStation.DOCK_STATION_TYPE:
                    stationRow["urls"].append(self.qr("Dock", "dock", station.station_id, msUrl))
                    stationRow["urls"].append(self.qr("Latch", "latch", station.station_id, msUrl))
                elif station.station_type == PiStation.SECURE_STATION_TYPE:
                    stationRow["urls"].append(self.qr("Open", "open", station.station_id, msUrl))
                    stationRow["urls"].append(self.qr("Secure", "secure", station.station_id, msUrl))
                elif station.station_type == PiStation.RETURN_STATION_TYPE:
                    stationRow["urls"].append(self.qr("Return", "return", station.station_id, msUrl))
                    
                self.context["station_table"].append(stationRow)

            return render(request, "piservice/station.html", self.context)
        else:
            return render(request, "piservice/libraryTest.html", self.context)
    
    def qr(self, label, path, stationId, baseUrl):
        """ Build the QR service request URL """
        url = self.QR_SERVICE_REQUEST_URL + urlquote("{}/{}/{}/".format(baseUrl, path, stationId))
        return {"label": label, "url": url }
    
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
#                           status=PiEvent.WARNING_STATUS,
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
                          status=PiEvent.WARNING_STATUS,
                          message="Failed to retrieve Team '{}' from the database".format(team_passcode),
                         )
            self.jsonResponse["message"] = "Invalid team_passcode: '{}'".format(team_passcode)
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
        # We are allowing resgistration but it now generates a new code for the new registration 
        # to ensure the team is only using one device at a time
        #if team.reg_code is not None and team.reg_code != "":
        #    # Failed:  Record the transaction and what went wrong
        #    self.addEvent(data=request.body,
        #                  status=PiEvent.INFO_STATUS,
        #                  message="Device {} already registered to Team {}".format(team.reg_code, team.pass_code),
        #                 )
        #    self.jsonResponse["message"] = "You already have a device registered.  You must Unregister it before Registering another device.".format(team_passcode)
        #    return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
            
        # Create a unique registration code for this Team's registration
        team.reg_code = Team.generateRegCode()

        dataToStore = json.loads(request.body)  # POST data (in JSON format)
        dataToStore["REMOTE_ADDR"] = request.META["REMOTE_ADDR"]  # IP address of sender

        # Succeeded:  Record the transaction and update the team record
        event = self.addEvent(team=team,
                              data=json.dumps(dataToStore),
                              status=PiEvent.INFO_STATUS,
                              message="Team '{}' Registered with brata_version '{}'. Assigned reg_code {}.".format(team.name, "m.brata_version", team.reg_code),
                             )
        
#         self.jsonResponse["message"] = "DEBUG"
#         return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
    
        team.registered = event.id  # not checking for multiple registrations, so multiple is ok
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
                          status=PiEvent.WARNING_STATUS,
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
                          status=PiEvent.WARNING_STATUS,
                          message="Failed to retrieve Team from the database with reg_code {}".format(reg_code),
                         )
            self.jsonResponse["message"] = "Unable to find registered device to unregister."
            self.jsonResponse["reg_code"] = data["reg_code"]  # return the reg_code that was sent
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
        
        # Succeeded:  Record the transaction and update the team record
        event = self.addEvent(team=team,
                              data=request.body,
                              status=PiEvent.INFO_STATUS,
                              message="Team '{}' Unregistered device with reg_code '{}'.".format(team.name, team.reg_code),
                             )
        
        # Erase the reg_code
        team.reg_code = ""
        
#         self.jsonResponse["message"] = "DEBUG"
#         return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
    
        team.registered = 0  # store the Unregister event in the registered field
        team.save()
        
        # Send a success response
        self.jsonResponse["message"] = "You have unregistered your BRATA device.  You may re-register it or register a different BRATA device."
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class Reset(JSONHandlerView):
    """ A class-based view to handle a BRATA Reset message.
    
        The client sends a POST message with the following JSON data:
        {
            "message":  "",
            "reg_code":  ""
        }
        and the end of the url is the team_passcode
        
        The MS sends the following response on success:
        {
            "reg_code":  "",
            "message":   "All team data for '<team_name>' was reset."
        }
    """
    def __init__(self):
        """ Initialize the base class with the type of message we will handle
            and the HTTP methods that we will accept.
        """
        super(Reset, self).__init__(PiEvent.RESET_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, team_passcode, *args, **kwargs):
        """ Handle the Registration POST message and update the database """
        super(Reset, self).post(request, *args, **kwargs)

        # Retrieve the Team record using the team_passcode from the Register request
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
                          status=PiEvent.WARNING_STATUS,
                          message="Failed to retrieve Team '{}' from the database".format(team_passcode),
                         )
            self.jsonResponse["message"] = "Invalid team_passcode: '{}'".format(team_passcode)
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)

        # Find allthe db records for the team and delete them
        try:
            teamRecords = PiEvent.objects.filter(team=team)
            teamRecords.exclude(type=PiEvent.ADDTEAM_TYPE).exclude(type=PiEvent.REGISTER_MSG_TYPE)
            teamRecords.delete()
        except:
            # If nothing found then just nothing to do
            pass        

        # Succeeded:  Record the transaction and update the team record
        event = self.addEvent(team=team,
                              data=request.body,
                              status=PiEvent.INFO_STATUS,
                              message="Team '{}' Reset by ip '{}'".format(team.name, request.META["REMOTE_ADDR"]),
                             )
        
        # Send a success response
        self.jsonResponse["reg_code"] = team.reg_code
        message = "All team data for '{}' was reset except registration.".format(team.name)
        self.jsonResponse["message"] = cipher(message)
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
            station_id   = data["station_id"].lower()
            station_type = data["station_type"].lower().capitalize()
            serial_num   = data["station_serial"]
            url          = data["station_url"] if "station_url" in data else ""
        except KeyError:
            # Send a fail response
            self.addEvent(data=request.body,
                          status=PiEvent.WARNING_STATUS,
                          message="Badly formed request",
                          )
            self.jsonResponse["message"] = "Badly formed request: {}".format(repr(data))
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
    
        # Validate the source of the message
        senderIP = request.META["REMOTE_ADDR"]  # IP address of sender
        if not PiStation.allowedHost(senderIP) or not PiStation.allowedSerialNum(serial_num):
            # Send a fail response
            self.addEvent(data=request.body,
                          status=PiEvent.WARNING_STATUS,
                          message="Join request from invalid host ({}) or serial_num ({}).  See MS setting STATION_IPS and STATION_SERIAL_NUMS.".format(senderIP, serial_num),
                         )
            self.jsonResponse["message"] = "Join request from invalid host ({}) or serial_num ({})".format(senderIP, serial_num)
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
        
        # Retrieve existing PiStation record or create a new one
        try:
            station = PiStation.objects.get(serial_num=serial_num)
        except ObjectDoesNotExist:
            station = PiStation(host=senderIP, station_id=station_id, station_type=station_type, serial_num=serial_num, url=url)
            station.save()
        
        # Succeeded:  Record the transaction and update the station record
        station.station_id = station_id #station.setStationId()
        station.joined = self.addEvent(pi=station,
                                       data=request.body,
                                       status=PiEvent.INFO_STATUS,
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
                          status=PiEvent.WARNING_STATUS,
                          message="Heartbeat received from invalid host: {}, station_id {}.  See MS setting STATION_IPS.".format(senderIP, station_id),
                         )
            self.jsonResponse["message"] = "Heartbeat message from unrecognized station: {} at address {}".format(station_id, senderIP)
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
        
#         # Succeeded:  Record the transaction and update the station record
#         event = self.addEvent(pi=station,

#                               data=request.body,
#                               status=PiEvent.INFO_STATUS,
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
                          status=PiEvent.WARNING_STATUS,
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
                          status=PiEvent.WARNING_STATUS,
                          message="Could not find a valid station: {}".format(station_id),
                         )
            self.jsonResponse["message"] = "Could not find a valid station: {}".format(station_id, repr(data))
            return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=400)
        
        # Succeeded:  Record the transaction and update the station record
        event = self.addEvent(pi=station,
                              data=request.body,
                              status=PiEvent.INFO_STATUS,
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
    
    def post(self, request, station_id, vertex, *args, **kwargs):
        """ Handle the POST message and update the database """
        super(AtWaypoint, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        m,response = self.validateJSONFields(request, ("reg_code",))
        if m is None:
            return response

        message="StartChallenge msg received from {}".format(m.reg_code)

        # Get the station from the station_id
        station, response = self.getStationFromStationId(station_id, request.body)
        if station is None:
            return response

        team, response = self.getTeamFromRegCode(m.reg_code, request.body)
        if team is None:
            return response

        # get the initial parameters from the start_challenge event
        # find the event and get the parameters out of the JSON data
        try:
            startRequests = PiEvent.objects.filter((
                Q(type=PiEvent.START_CHALLENGE_MSG_TYPE)|
                Q(type=PiEvent.SUBMIT_MSG_TYPE)|
                Q(type=PiEvent.STATION_SUBMIT_MSG_TYPE)) &
                Q(pi=station) &
                Q(team=team)
                ).order_by('-time')[:1]
        except:
            message = "No start found at this station"
            # TODO handle error
            event = PiEvent.addEvent(type=PiEvent.AT_WAYPOINT_MSG_TYPE,
                              pi=station,
                              data=json.dumps({"station":station_id,"reg_code":m.reg_code}),
                              status=PiEvent.INFO_STATUS,
                              message=message,
                             )

        try:
            data = json.loads(startRequests[0].data)
        except:
            message = "problem loading start request data"
        if data is None:
            # TODO make error message
            return response

        launchParams = data["LAUNCH_PARAMS"]
        currentVertexNumber = data["CURRENT_VERTEX_NUMBER"]
        attemptNumber = data["ATTEMPT_NUMBER"]
        currentVertex = launchParams[currentVertexNumber]

        # Todo determine if wasCorrect and if three retries have been made for this coordinate
        wasCorrect = True
        wrongVertex = False
        if currentVertex[0] != vertex:
            wasCorrect = False
            if False: # TODO establish if even in the right area
                wrongVertex = True # they are in completely the wrong place not just a decoy
        retry = True
        if attemptNumber == 2: # in other words there were already 2 attempts so this is the third
           retry = False
        # Assume is a retry case
        type=PiEvent.STATION_SUBMIT_MSG_TYPE
        status = PiEvent.INFO_STATUS

        # Need to make sure these status make it in the log and back to the user regardless of station coms
        # this is what the scoring is based on
        if wasCorrect:
            # Succeeded:  Record the transaction and update the station record
            status = PiEvent.SUCCESS_STATUS
            type=PiEvent.SUBMIT_MSG_TYPE
            if currentVertexNumber == 0 or currentVertex == 1:
                message = "Correct! Continue to the next vertex"
            elif currentVertexNumber == 2:
                message = "Correct! Continue to the center"
            else: # currentVertexNumber == 3:
                message = "Correct! Continue to the next Challenge"
            currentVertexNumber += 1
            attemptNumber = 0
        elif retry:
            message = "Decoy, try again!"
            #TODO alternative retries
            if wrongVertex and currentVertexNumber == 0:
                message = "Sorry, not the Origin; Go to the Origin"
            elif wrongVertex and (currentVertexNumber == 1 or currentVertexNumber == 2):
                message = "Sorry, not a vertex; Go to the right vertex"
            elif wrongVertex:
                message = "Sorry, not the Center; Go to the Center"
            attemptNumber += 1
        else:
            # Post failures so scoring can keep track of them
            status = PiEvent.FAIL_STATUS
            type=PiEvent.SUBMIT_MSG_TYPE
            if currentVertexNumber == 0 or currentVertex == 1:
                message = "Sorry, go to the next vertex"
            elif currentVertexNumber == 2:
                message = "Sorry, go to the center"
            else: # currentVertexNumber == 3:
                #This is the final signal it is completely over
                message = "Sorry, go to the next Challenge"
            currentVertexNumber += 1
            attemptNumber = 0

        startData = json.dumps({
                "LAUNCH_PARAMS": launchParams,
                "CURRENT_VERTEX_NUMBER": currentVertexNumber,
                "ATTEMPT_NUMBER": attemptNumber,
            })

        # SUBMIT_MSG_TYPE is used for success for failure tracking for scoring
        event = PiEvent.addEvent(type=type,
                              team=team,
                              pi=station,
                              data=startData,
                              status=status,
                              message=message,
                             )
        
        # Send a success response
        self.jsonResponse["message"] = cipher(message)
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class StartChallenge(JSONHandlerView):
    """ A class-based view to handle a BRATA StartChallenge message.
    
        The client sends a POST message with the following JSON data:
        {
            "reg_code":        "current reg_code",
            "message":         ""
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
        
        message="StartChallenge msg received from {}".format(m.reg_code)

        # Get the station from the station_id
        station, response = self.getStationFromStationId(station_id, request.body)
        if station is None:
            return response

        team, response = self.getTeamFromRegCode(m.reg_code, request.body)
        if team is None:
            return response

        # assuming all goes well
        data=request.body
        # INFO because success is reserved for final event evaluation as SUCCESS or FAIL
        status=PiEvent.INFO_STATUS

	# Send message to the Pi this team is registered with to start the simulation
        url = "{}/start_challenge".format(station.url)
        headers = { "Content-type": "application/json", "Accept": "application.json" }
        shouldCallStation = True

        if station.station_type == "Launch":
            # Get set of random parameters
            # Randomly select a triangle from the next group of triangles by color
            launchParamsList = Setting.getLaunchParams()
            # Pick at random
            launchParams=random.choice(launchParamsList)
            shouldCallStation = False
            currentVertexNumber = 0
            attemptNumber = 0
            startData = json.dumps({
                    "LAUNCH_PARAMS": launchParams,
                    "CURRENT_VERTEX_NUMBER": currentVertexNumber,
                    "ATTEMPT_NUMBER": attemptNumber,
                })
            origin = launchParams[0]
            lat = origin[1]
            lon = origin[2]
            angle = origin[3]
            side = launchParams[3][1]
            tmpList = []
            tmpList.append(origin[0])
            color = tmpList[0]
            # NOTE this is just text
            message = "Layout the launch site at [LAT={}] [LON={}] [ROT={}] [SIDE={}] [COLOR={}]".format(lat, lon, angle, side, color)
        elif station.station_type == "Dock":
            jsonData = json.dumps({
                 "message_version": "0",
                 "message_timestamp": self.getDateTime(),
                 "team_name": team.name,
               })
            # Get random parameters
            dockParams = Setting.getDockParams()
            sets = dockParams["sets"]
            randomSet = random.choice(sets)
          
            aft = "{:.3f}".format(randomSet["a_aft"])
            fore = "{:.3f}".format(randomSet["a_fore"])
            fuel = "{0:05.2f}".format(randomSet["f_qty"])
            rate = "{0:05.2f}".format(randomSet["f_rate"])
            tape = "{}".format(randomSet["tape_id"])
            dist = "{}".format(randomSet["tape_len"])

            message = "Dock using [TAPE={}] [AFT={}] [FORE={}] [FUEL={}] [F-RATE={}]".format(tape, aft, fore, fuel, rate)
            startData = json.dumps({
                 "AFT": aft,
                 "FORE": fore,
                 "FUEL": fuel,
                 "F_RATE": rate,
                 "DIST": dist,
               })

        elif station.station_type == "Secure":
            # Get random parameters
            lock, tone = Setting.getSecureParams()
            jsonData = json.dumps({
                 "message_version": "0",
                 "message_timestamp": self.getDateTime(),
                 "secure_tone_pattern": tone,
                   })
            startData = json.dumps({
                 "lock": lock,
                 "tone": tone,})
            message="Attach the mic cord and determine the 4 Lock Digits, then scan the Open QR Code"
        elif station.station_type == "Return":
            # Get parameters for this particular station
            params = Setting.getReturnParams(station_id=station.station_id)
            if not (params is None):
              jsonData = json.dumps({
                 "message_version": "0",
                 "message_timestamp": self.getDateTime(),
                 "return_guidance_pattern": [params[0], params[1], params[2], params[3], params[4], params[5]],
                   })
              startData = jsonData
              message="Measure return angle, determine guidance computer parameters, then enter them into the guidance computer. Scan Return QR Code when done."
            else:
              shouldCallStation = False
              status = PiEvent.WARNING_STATUS
              startData = ""
              message="Invalid StationID {}. Contact a competition official.".format(station.station_id)

        else:
            shouldCallStation = False
            status = PiEvent.WARNING_STATUS
            startData = ""
            message="Invalid StationID {}. Contact a competition official.".format(station.station_id)

        # Record the transaction status
        event = self.addEvent(team=team,
                              pi=station,
                              data=startData,
                              status=status,
                              message=message,
                             )

	if shouldCallStation:
            response = requests.post(url, data=jsonData, headers=headers)
            if response.status_code != 200:
                message = "Could not contact station. Contact a competition official."	
                status = PiEvent.WARNING_STATUS
                data = response

                # Record the transaction status
                event = self.addEvent(
                              team=team,
                              pi=station,
                              data=data,
                              status=status,
                              message=message,
                             )
        
        # Send a success response
        self.jsonResponse["message"] = cipher(message)
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

        team, response = self.getTeamFromRegCode(m.reg_code, request.body)
        if team is None:
            return response
        
        # Get the station from the station_id
        station, response = self.getStationFromStationId(station_id, request.body) 
        if station is None:
            return response
        
        # setup assuming all goes well
        message = "Docking Parameters received!"
        status=PiEvent.INFO_STATUS
        data=request.body

        # get submitted params from the message
        messageData, response = self.getFieldsFromBrataMessage(m.message, ("T-AFT", "T-COAST", "T-FORE",))
        if messageData is None:
           return response

        t_aft = messageData.TAFT
        t_coast = messageData.TCOAST
        t_fore = messageData.TFORE

        # get the initial parameters from the start_challenge event
        # find the event and get the parameters out of the JSON data
        try:
            startRequests = PiEvent.objects.filter(type=PiEvent.START_CHALLENGE_MSG_TYPE, pi=station, team=team).order_by('-time')[:1]
        except:
            message = "No start found at this station"
            # TODO handle error
        try:
            data = json.loads(startRequests[0].data)
        except:
            message = "problem loading start request data"
        if data is None:
            # TODO make error message
            return response

        a_aft = data["AFT"]
        a_fore = data["FORE"]
        dist = data["DIST"]
        r_fuel = data["F_RATE"]
        q_fuel = data["FUEL"]

        dockParams = Setting.getDockParams()
        min_dock = "{:.2f}".format(dockParams["min_dock"])
        max_dock = "{:.1f}".format(dockParams["max_dock"])
        init_vel = "{:.1f}".format(dockParams["init_vel"])
        sim_time = "{0:0>2}".format(dockParams["sim_time"])
        
	# Send message to the Pi this team is registered with to start the simulation
        url = "{}/post_challenge".format(station.url)
        headers = { "Content-type": "application/json", "Accept": "application.json" }
        jsonData = json.dumps({
                 "t_aft": t_aft,
                 "t_coast": t_coast,
                 "t_fore": t_fore,
                 "a_aft": a_aft,
                 "a_fore": a_fore,
                 "r_fuel": r_fuel,
                 "q_fuel": q_fuel,
                 "dist": dist,
                 "v_min": min_dock,
                 "v_max": max_dock,
                 "v_init": init_vel,
                 "t_sim": sim_time,
               })
	response = requests.post(url, data=jsonData, headers=headers)
        if response.status_code != 200:
            message = "Could not contact simulation server.  Contact a competition official."	
            status = PiEvent.WARNING_STATUS
            data = response

        # If all went well then store what params were assigned to the team
        data = jsonData

        # Record the transaction and update the station record
        event = self.addEvent(team=team,
                              pi=station,
                              data=data,
                              status=status,
                              message=message,
                             )
                    
        # Send a success response
        self.jsonResponse["message"] = cipher(message)

        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class Latch(JSONHandlerView):
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
        super(Latch, self).__init__(PiEvent.LATCH_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, station_id, *args, **kwargs):
        """ Handle the POST message and update the database """
        super(Latch, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        m,response = self.validateJSONFields(request, ("reg_code","message",))
        if m is None:
            return response

        team, response = self.getTeamFromRegCode(m.reg_code, request.body)
        if team is None:
            return response
        
        # Get the station from the station_id
        station, response = self.getStationFromStationId(station_id, request.body)        
        if station is None:
            return response
        
        wasCorrect, retry, lastAnswer, lastAttemptData, response = self.getStatus(team, station)
        if wasCorrect is None:
            return response

        # Need to make sure these status make it in the log and back to the user regardless of station coms
        # this is what the scoring is based on and needs to include the time for docking including penalty
        if wasCorrect:
            # Succeeded:  Record the transaction and update the station record
            message = "Docking latches engaged! Continue to next Challenge!"
            status = PiEvent.SUCCESS_STATUS
        else:
            # Post failures so scoring can keep track of them
            status = PiEvent.FAIL_STATUS
            if retry:
                # Get random parameters
                dockParams = Setting.getDockParams()
                sets = dockParams["sets"]
                randomSet = random.choice(sets)
          
                aft = "{:.3f}".format(randomSet["a_aft"])
                fore = "{:.3f}".format(randomSet["a_fore"])
                fuel = "{0:0>2.2f}".format(randomSet["f_qty"])
                rate = "{0:0>2.3f}".format(randomSet["f_rate"])
                tape = "{0:0>2}".format(randomSet["tape_id"])
                dist = "{0:0>2}".format(randomSet["tape_len"])

                message = "Dock using [TAPE={}] [AFT={}] [FORE={}] [FUEL={}] [F-RATE={}]".format(tape, aft, fore, fuel, rate)
                startData = json.dumps({
                     "AFT": aft,
                     "FORE": fore,
                     "FUEL": fuel,
                     "F_RATE": rate,
                     "DIST": dist,
                   })
                event = PiEvent.addEvent(type=PiEvent.START_CHALLENGE_MSG_TYPE,
                              team=team,
                              pi=station,
                              data=startData,
                              status=PiEvent.INFO_STATUS,
                              message=message,
                             )
            else:
                message = "Failed! Go to the next Challenge!"

        # figure out if actual docking time requires penalty
        # TODO change the reported time in data            
        failMessage = json.loads(lastAttemptData)["fail_message"]
	jsonTime = json.dumps({
             "candidate_answer": lastAnswer,
             "fail_message": failMessage,
           })
        data = jsonTime
        
        # SUBMIT_MSG_TYPE is used for success for failure tracking for scoring
        event = PiEvent.addEvent(type=PiEvent.SUBMIT_MSG_TYPE,
                              team=team,
                              pi=station,
                              data=data,
                              status=status,
                              message=message,
                             )
        
	# Send message to the Pi this team is registered with to restart the simulation no matter what
        url = "{}/reset/31415".format(station.url)
        headers = { "Content-type": "application/json", "Accept": "application.json" }
        jsonData = json.dumps({})
	response = requests.post(url, data=jsonData, headers=headers)
        if response.status_code != 200:
            errorMessage = "Could not contact station. Contact a competition official."	
            errorStatus = PiEvent.WARNING_STATUS
            data = response
            event = self.addEvent(team=team,
                              pi=station,
                              data=data,
                              status=errorStatus,
                              message=errorMessage,
                             )
            if retry:
                # We need to make the team aware as there is a problem that keeps them from continuing
                self.jsonResponse["message"] = cipher(errorMessage)
                return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

        if retry:
            # take it from the top
            url = "{}/start_challenge".format(station.url)
            headers = { "Content-type": "application/json", "Accept": "application.json" }
	    jsonData = json.dumps({
                 "message_version": "0",
                 "message_timestamp": self.getDateTime(),
                 "team_name": team.name,
               })

            response = requests.post(url, data=jsonData, headers=headers)
            if response.status_code != 200:
                message = "Could not contact station. Contact a competition official."	
                status = PiEvent.WARNING_STATUS
                data = response
                event = self.addEvent(team=team,
                              pi=station,
                              data=data,
                              status=status,
                              message=message,
                             )
        
        # Send a response
        self.jsonResponse["message"] = cipher(message)
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class Open(JSONHandlerView):
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
        super(Open, self).__init__(PiEvent.OPEN_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, station_id, *args, **kwargs):
        """ Handle the POST message and update the database """
        super(Open, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        m,response = self.validateJSONFields(request, ("reg_code","message",))
        if m is None:
            return response

        team, response = self.getTeamFromRegCode(m.reg_code, request.body)
        if team is None:
            return response
        
        # Get the station from the station_id
        station, response = self.getStationFromStationId(station_id, request.body)
        if station is None:
            return response

        message = "Photodetector enabled: send Lock Digit pulses now!"
        status=PiEvent.INFO_STATUS
        httpStatus = 200

        # get the initial parameters from the start_challenge event
        # find the event and get the parameters out of the JSON data
        try:
            startRequests = PiEvent.objects.filter(type=PiEvent.START_CHALLENGE_MSG_TYPE, pi=station, team=team).order_by('-time')[:1]
        except:
            message = "No start found at this station"
            # TODO handle error
        data = json.loads(startRequests[0].data)
        if data is None:
            # TODO make error message
            return response

        lock = data["lock"]

	# Send message to the Pi this team is registered with to start the simulation
        url = "{}/post_challenge".format(station.url)
        headers = { "Content-type": "application/json", "Accept": "application.json" }
        data = json.dumps({
                 "message_version": "0",
                 "message_timestamp": self.getDateTime(),
                 "secure_pulse_pattern": lock,
                 "secure_max_pulse_width": "100",
                 "secure_max_gap": "10",
                 "secure_min_gap": "10",
               })
	response = requests.post(url, data=data, headers=headers)

        data = request.body
        if response.status_code != 200:
            message = "Could not contact station server.  Contact a competition official."	
            status=PiEvent.WARNING_STATUS
            data = response
            
        # Record the transaction and update the station record
        event = self.addEvent(team=team,
                              pi=station,
                              data=data,
                              status=status,
                              message=message,
                             )
        
        # Send a success response
        self.jsonResponse["message"] = cipher(message)
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=httpStatus)

#----------------------------------------------------------------------------
class Secure(JSONHandlerView):
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
        super(Secure, self).__init__(PiEvent.SECURE_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, station_id, *args, **kwargs):
        """ Handle the POST message and update the database """
        super(Secure, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        m,response = self.validateJSONFields(request, ("reg_code","message",))
        if m is None:
            return response

        team, response = self.getTeamFromRegCode(m.reg_code, request.body)
        if team is None:
           return response

        station, response = self.getStationFromStationId(station_id, request.body)
        if station is None:
            return response

        wasCorrect, retry, lastAnswer, lastAttemptData, response = self.getStatus(team, station)
        if wasCorrect is None:
            return response

        if wasCorrect:
            # Succeeded:  Record the transaction and update the station record
            status=PiEvent.SUCCESS_STATUS
            message = "Correct! Go to the next Challenge!"
        else:
            # failed
            status=PiEvent.FAIL_STATUS
            if retry:
                message = "Try again by listening to tones again (optional) and scanning Open QR Code to re-enable photodetector"

   	        # Restart since they failed < 3 times 
                url = "{}/start_challenge".format(station.url)
                headers = { "Content-type": "application/json", "Accept": "application.json" }
                # Go back to generating tones they had before by extracting from their previous start_challenge params
                try:
                    startRequests = PiEvent.objects.filter(type=PiEvent.START_CHALLENGE_MSG_TYPE, pi=station, team=team).order_by('-time')[:1]
                except:
                    message = "No start found at this station"
                    # TODO handle error
                data = json.loads(startRequests[0].data)
                if data is None:
                    # TODO make error message
                    return response

                tone = data["tone"]
                # TODO
                data = json.dumps({
                    "message_version": "0",
                    "message_timestamp": self.getDateTime(),
                    "secure_tone_pattern": tone,
                   })
                response = requests.post(url, data=data, headers=headers)
                if response.status_code != 200:
                    message = "Could not contact simulation server.  Contact a competition official."	
            else:
                message = "Failed! Go to the next Challenge!"

        # SUBMIT_MSG_TYPE is used for success for failure tracking for scoring
        event = PiEvent.addEvent(type=PiEvent.SUBMIT_MSG_TYPE,
                              team=team,
                              pi=station,
                              data=request.body,
                              status=status,
                              message=message,
                              )
        if not retry:
          # Send message to the Pi this team is registered with to restart the simulation
          # if it doesn't though we don't care the next start should fix it
          url = "{}/reset/31415".format(station.url)
          headers = { "Content-type": "application/json", "Accept": "application.json" }
          jsonData = json.dumps({})
	  response = requests.post(url, data=jsonData, headers=headers)
          if response.status_code != 200:
            errorMessage = "Could not contact station. Contact a competition official."	
            errorStatus = PiEvent.WARNING_STATUS
            data = response
            event = self.addEvent(team=team,
                              pi=station,
                              data=data,
                              status=errorStatus,
                              message=errorMessage,
                             )
 
        # Send response
        self.jsonResponse["message"] = cipher(message)
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class ReturnToEarth(JSONHandlerView):
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
        super(ReturnToEarth, self).__init__(PiEvent.RETURN_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, station_id, *args, **kwargs):
        """ Handle the POST message and update the database """
        super(ReturnToEarth, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        m,response = self.validateJSONFields(request, ("reg_code","message",))
        if m is None:
            return response

        team, response = self.getTeamFromRegCode(m.reg_code, request.body)
        if team is None:
           return response

        station, response = self.getStationFromStationId(station_id, request.body)
        if station is None:
            return response

        wasCorrect, retry, lastAnswer, lastAttemptData, response = self.getStatus(team, station)
        if wasCorrect is None:
            return response

        if wasCorrect:
            # Succeeded:  Record the transaction and update the station record
            status=PiEvent.SUCCESS_STATUS
            message = "Correct! You have returned successfully!"
        else:
            # failed
            if retry:
   	        # Restart since they failed < 3 times 
                # Store failure no matter what for score keeping
                status=PiEvent.FAIL_STATUS
                # This is the message to send assuming restart of the station works
                message = "Try again! A bit signed but still alive!"
            else:
                status=PiEvent.FAIL_STATUS
                message = "Failed! Too bad but all done."

        # SUBMIT_MSG_TYPE is used for success for failure tracking for scoring
        event = PiEvent.addEvent(type=PiEvent.SUBMIT_MSG_TYPE,
                              team=team,
                              pi=station,
                              data=request.body,
                              status=status,
                              message=message,
                              )

        url = "{}/start_challenge".format(station.url)
        if retry:
            # Get parameters for this particular station
            params = Setting.getReturnParams(station_id=station.station_id)
            if not (params is None):
              jsonData = json.dumps({
                 "message_version": "0",
                 "message_timestamp": self.getDateTime(),
                 "return_guidance_pattern": [params[0], params[1], params[2], params[3], params[4], params[5]],
                   })
              startData = jsonData
              message="Measure return angle, determine guidance computer parameters, then enter them into the guidance computer. Scan Return QR Code when done."
            else:
              status = PiEvent.WARNING_STATUS
              message="Invalid StationID {}. Contact a competition official.".format(station.station_id)
              data = response
              event = self.addEvent(team=team,
                              pi=station,
                              data=data,
                              status=status,
                              message=message,
                             )
              self.jsonResponse["message"] = cipher(message)
              return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)
        else: 
          # Send message to the Pi this team is registered with to restart the simulation no matter what
          url = "{}/reset/31415".format(station.url)
          jsonData = json.dumps({})

        # Either way we call the pi
        headers = { "Content-type": "application/json", "Accept": "application.json" }
	response = requests.post(url, data=jsonData, headers=headers)
        if response.status_code != 200:
            errorMessage = "Could not contact station. Contact a competition official."	
            errorStatus = PiEvent.WARNING_STATUS
            data = response
            event = self.addEvent(team=team,
                              pi=station,
                              data=data,
                              status=errorStatus,
                              message=errorMessage,
                             )
            if retry:
                # We need to make the team aware as there is a problem that keeps them from continuing
                self.jsonResponse["message"] = cipher(errorMessage)
                return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

        # Send response
        self.jsonResponse["message"] = cipher(message)
        return HttpResponse(json.dumps(self.jsonResponse), content_type="application/json", status=200)

#----------------------------------------------------------------------------
class Submit(JSONHandlerView):
    """ A class-based view to handle a Stations Submit message.
    
        The client sends a POST message with the following JSON data:
        {
            "station_id":        "id of the station",
        }
        
        The MS sends the following response on success:
        {
            "challenge_complete":  "True"
        }
    """
    def __init__(self):
        super(Submit, self).__init__(PiEvent.STATION_SUBMIT_MSG_TYPE, methods=[self.POST])
    
    def post(self, request, *args, **kwargs):
        """ Handle the POST message and update the database """
        super(Submit, self).post(request, *args, **kwargs)

        # Get input parameters from URL and/or POST data
        m,response = self.validateJSONFields(request, ("station_id","is_correct","fail_message","candidate_answer"))
        if m is None:
            return response

        station, response = self.getStationFromStationId(m.station_id, request.body)
        if station is None:
            return response

        # figure out which team is at that station based on the last transation for that station
        # TODO
        try:
            startRequests = PiEvent.objects.filter(type=PiEvent.START_CHALLENGE_MSG_TYPE, pi=station).order_by('-time')[:1]
        except:
            message = "No start found at this station"
        team = startRequests[0].team        

        # Record the transaction and update the station record
        # Note we store the entire response to make data extraction during last QR scan eaiser
        event = self.addEvent(team=team,
                              pi=station,
                              data=request.body,
                              status=PiEvent.INFO_STATUS,
                              message="Submit msg received from {}".format(m.station_id),
                             )
        
        # Figure out what to do next
        wasCorrect, retry, lastAnswer, lastAttemptData, response = self.getStatus(team, station)
        if wasCorrect is None:
            return response

        challengeComplete = wasCorrect or not retry
        self.jsonResponse["challenge_complete"] = "{}".format(challengeComplete)
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
                          status=PiEvent.WARNING_STATUS,
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
        
        team.registered = event.id  # not checking for multiple registrations, so multiple is ok
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

#----------------------------------------------------------------------------
class QRCode(JSONHandlerView):
    def get(self, request, *args, **kwargs):
        """ Handle a GET message
            Create a QR code and display it in a web page.
            
            Return an HttpResponse object.
        """
        # note this tries to figure out the data automagically
        # so provide a URL and will set the qrcode type to URL if just text you get text
        strToEncode = request.GET.get('chl', '')
        #image = self.makeQrCodeImage(strToEncode)
        #html = self.makeInlineImageTag(image)
        
        #if true:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=5, border=4)
        qr.add_data(strToEncode)
        qr.make(fit=True)
        image = qr.make_image()
        response = HttpResponse(content_type="image/png")
        image.save(response, "PNG")
        #else:
            # TODO seems it would be more efficient to make this SVG
        #    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=5, border=4, image_factory=qrcode.image.svg.SvgImage)
        #    qr.add_data(strToEncode)
        #    qr.make(fit=True)
        #    image = qr.make_image()    
        #    response = HttpResponse(content_type="image/svg+xml")
            #response['Content-Disposition'] = 'out.svg'
        #    image.save(response, "XML")
        return response

#----------------------------------------------------------------------------
class QRCodeNew(JSONHandlerView):
#     def get(self, request, *args, **kwargs):
#         """ Handle a GET message """
#         # note this tries to figure out the data automagically
#         # so provide a URL and will set the qrcode type to URL if just text you get text
#         strToEncode = request.GET.get('chl', '')
#         # version 1 is the smallest possible goes up to 40
#         # default error correct is L for up to 7% errors, it is what we used before so no reason to go higher
#         # NOTE we tried for fun error correct up one level to M DO NOT DO IT!  It will kill the Pi.
#         # per the spec need to leave a border of at least 4 units
#         # size we used 350 in the past but seems to be taking long as well
#         qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=5, border=4, image_factory=qrcode.image.svg.SvgImage)
#         qr.add_data(strToEncode)
#         #qr.make(fit=True)
#         #image = qr.make_image()
#         #response = HttpResponse(content_type="image/png")
#         #image.save(response, "PNG")
#         # TODO seems it would be more efficient to make this SVG
#         image = qr.make(fit=True)
#         #image = qr.make(strToEncode, image_factory=qrcode.image.svg.SvgImage)
#         response = HttpResponse(content_type="image/svg+xml")
#         response['Content-Disposition'] = 'out.svg'
#         response.write(image)
#         return response

    def get(self, request, *args, **kwargs):
        """ Handle a GET message
            Create a QR code and return an image.
            
            Return an HttpResponse object containing the image.
        """
        # note this tries to figure out the data automagically
        # so provide a URL and will set the qrcode type to URL if just text you get text
        strToEncode = request.GET.get('chl', '')
        image = self.makeQrCodeImage(strToEncode)
        
        # Serialize the image data to a memory buffer
        imgdata = cStringIO.StringIO()
        imgType = "png"
        image.save(imgdata, format=imgType)
        imgdata.seek(0) # rewind to start of image data

        response = HttpResponse(content_type="image/" + imgType)
        response.write(imgdata.read())
        
#         # Include the following tag to cause the browser to display the Save dialog
#         response['Content-Disposition'] = "out." + imgType 
        return response

#         # Generate a simple HTML page containing a centered QR code image
#         # with centered text below it
#         html = self.makeInlineImageTag(image)
#         
#         response = HttpResponse(content_type="text/html")
#         response.write("<html><head></head><body>")
#         response.write('<div style="text-align: center;">')
#         response.write(html)
#         response.write('</div><div style="text-align: center;">')
#         response.write(strToEncode)
#         response.write("</div></body></html>")
#         return response

    def makeQrCodeImage(self, text, rgb=False, boxSizePx=5):
        """ Create a QR code image representing 'text'.
            If rgb is True, convert the resulting image from
            black-and-white to RGB.
            
            Return a PIL image.
        """
        # version 1 is the smallest possible goes up to 40
        # default error correct is L for up to 7% errors, it is what we used before so no reason to go higher
        # NOTE we tried for fun error correct up one level to M DO NOT DO IT!  It will kill the Pi.
        # per the spec need to leave a border of at least 4 units
        # size we used 350 in the past but seems to be taking long as well
        qr = qrcode.QRCode(version=None,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=boxSizePx,
                           border=4)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image()
        if rgb:
            img = img.convert("RGB")
        return img

    def makeInlineImageTag(self, pilImage, altText="embedded image", imgType="png"):
        """ Create an <img ...> tag with an inline data URL that contains an image.
            The tag that is created looks like this:
                <img src="data:image/png;base64,iVBORw0KGg ... kJgxg==" alt="embedded image" />
            The image data are contained in the URL, so it does not do a server access.
            
            See: http://www.websiteoptimization.com/speed/tweak/inline-images/
            
            Return a string containing the HTML tag
        """
        # Serialize the image data to a memory buffer
        imgdata = cStringIO.StringIO()
        pilImage.save(imgdata, format=imgType)
        imgdata.seek(0) # rewind to start of image data
        
        # Encode the binary string
        b64Image = base64.b64encode(imgdata.getvalue())
        imgdata.close() # free the buffer
        
        return '<img src="data:image/{};base64,{}" alt="{}" />'.format(imgType, b64Image, altText)

from django.shortcuts import render, HttpResponse
from django.views.generic import View


#----------------------------------------------------------------------------
class Scoreboard(View):
    """ Display the scoreboard page.
        Updating is driven by the page making REST requests.
    """
    context = {}
    def get(self, request):
        return render(request, "scoreboard/scoreboard.html", self.context)

#----------------------------------------------------------------------------
class Scores(View):
    """ A REST request to get scores from the database for the leaderboard """
    def get(self, request):
        """ Retrieve score information from the database and return it """
        # Get scores from the database
        # Format scores into JSON
        # Return
        return HttpResponse("")

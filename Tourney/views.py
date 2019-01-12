# Create your views here.
from django.views import generic

from Tourney.models import Tournament


class TournamentViewAll(generic.ListView):
    model = Tournament
    queryset = Tournament.objects.all()
    template_name = "tournaments/tournaments-view-all.html"


class TournamentView(generic.ListView):
    model = Tournament
    queryset = Tournament.objects.all()
    template_name = "tournaments/tournament-view.html"

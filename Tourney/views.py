# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic

from Tourney.models import Tournament, TournamentEntry, TournamentManager


class TournamentViewAll(generic.ListView):
    model = Tournament
    queryset = Tournament.objects.all()
    template_name = "tournaments/tournaments-view-all.html"


class TournamentView(generic.DetailView):
    model = Tournament
    queryset = Tournament.objects.all()
    template_name = "tournaments/tournament-view.html"


@login_required
def enter_tournament(request, pk):
    """For adding someone to a tournament"""
    if request.method == "POST":
        event = Tournament.objects.get(pk=pk)
        entry = request.user.profile
        try:
            TournamentManager.enter_tournament(event=event, entry=entry)
        except TournamentEntry.DoesNotExist:
            return False
        else:
            return redirect('Tourney:tournament-entry', pk=pk)

    return render(request, "tournaments/tournaments-view-all.html")

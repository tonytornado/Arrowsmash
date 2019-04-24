# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic

from League.models import League, LeagueEntry, LeagueManager, TrialManager, TrialEntry, Trial


class LeagueViewAll(generic.ListView):
    model = League
    queryset = League.objects.all()
    template_name = "leagues/league-view-all.html"


class LeagueView(generic.DetailView):
    model = League
    queryset = League.objects.all()
    template_name = "leagues/league-view.html"


class TrialViewAll(generic.ListView):
    model = Trial
    queryset = Trial.objects.all()
    template_name = "leagues/trial-view-all.html"


class TrialView(generic.DetailView):
    model = Trial
    queryset = Trial.objects.all()
    template_name = "leagues/trial-view.html"


@login_required
def enter_league(request, pk):
    """For adding someone to a League
    :param request: User stats
    :param pk: PK for league
    :return:
    """
    if request.method == "POST":
        event = League.objects.get(pk=pk)
        entry = request.user.profile
        try:
            LeagueManager.enter_League(event=event, entry=entry)
        except LeagueEntry.DoesNotExist:
            return False
        else:
            return redirect('League:league-entry', pk=pk)

    return render(request, "leagues/league-view-all.html")


@login_required
def add_trial(request, pk):
    """
    For adding a trial to your profile
    :param request: User stats
    :param pk: PK for the trial
    """
    if request.method == "POST":
        event = Trial.objects.get(pk=pk)
        dancer = request.user.profile
        try:
            TrialManager.start_trial(event=event, dancer=dancer)
        except TrialEntry.DoesNotExist:
            return False
        else:
            return redirect('League:trial-entry')

    return render(request, "leagues/trial-view-all.html")

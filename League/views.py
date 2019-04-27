from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
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


class LeagueCreate(generic.CreateView):
    model = League
    template_name = "leagues/league-submit.html"
    success_url = reverse_lazy("League:league-list")
    fields = ('name', 'organizer', 'mix', 'rules', 'competition_date_start', 'competition_date_end')

    def form_valid(self, form):
        # form.instance.player = self.request.user.profile
        return super().form_valid(form)


class TrialViewAll(generic.ListView):
    model = Trial
    queryset = Trial.objects.all()
    template_name = "leagues/trial-view-all.html"


class TrialView(generic.DetailView):
    model = Trial
    queryset = Trial.objects.all()
    template_name = "leagues/trial-view.html"


class TrialCreate(generic.CreateView):
    model = Trial


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
            messages.error(request, "ERROR: Something went wrong.")
            return redirect('League:league-view', pk)

    messages.success(request, "Success! You're in.")
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
            messages.error(request, "ERROR: Something went wrong.")
            return redirect('League:trial-view', pk)

    messages.success(request, "Success! You're in.")
    return render(request, "leagues/trial-view-all.html")

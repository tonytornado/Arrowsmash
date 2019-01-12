# Create your views here.
from django.views import generic

from Scores.models import Score


class ScoreListing(generic.ListView):
    model = Score
    queryset = Score.objects.all()
    template_name = "scores/score-list-all.html"


class ScoreDetail(generic.DetailView):
    model = Score
    queryset = Score.objects.all()
    template_name = "scores/score-detail.html"

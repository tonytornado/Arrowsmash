from django.urls import reverse_lazy
from django.views import generic
from rest_framework import generics

from Scores.forms import ScoreForm
from Scores.models import Score, SongChart
from Scores.serializers import SongChartSerializer


class ScoreListing(generic.ListView):
    model = Score
    queryset = Score.objects.order_by('date').all()
    template_name = "scores/score-list-all.html"


class ScoreDetail(generic.DetailView):
    model = Score
    queryset = Score.objects.all()
    template_name = "scores/score-detail.html"


class ScoreSubmit(generic.CreateView):
    model = Score
    form_class = ScoreForm
    queryset = Score.objects.order_by('song__name').all()
    template_name = "scores/score-submit.html"
    success_url = reverse_lazy('Scores:score-list')
    success_message = "Score submitted!"

    def form_valid(self, form):
        form.instance.player = self.request.user.profile
        return super().form_valid(form)


class SongDB(generic.ListView):
    model = SongChart
    queryset = SongChart.objects.all()
    template_name = "scores/score-song-list.html"


class JSONView(generics.ListAPIView):
    queryset = SongChart.objects.all()
    serializer_class = SongChartSerializer


class JSONDetailView(generics.RetrieveAPIView):
    queryset = SongChart.objects.all()
    serializer_class = SongChartSerializer

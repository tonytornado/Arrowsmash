from django.urls import reverse_lazy
from django.views import generic

from Scores.forms import ScoreForm
from Scores.models import Score, Song


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
    template_name = "scores/score-submit.html"
    success_url = reverse_lazy('Scores:score-list')

    def form_valid(self, form):
        form.instance.player = self.request.user.profile
        return super().form_valid(form)


class SongDB(generic.ListView):
    model = Song
    queryset = Song.objects.all()
    template_name = "scores/song_db.html"

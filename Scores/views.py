from django.urls import reverse_lazy
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


class ScoreSubmit(generic.CreateView):
    model = Score
    fields = ('song', 'score_rank', 'ex', 'proof')
    template_name = "generic/form.html"
    success_url = reverse_lazy('Scores:score-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.player = self.request.user.profile
        return super().form_valid(form)

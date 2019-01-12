from django.contrib import admin

from Tourney.models import Tournament, TournamentEntry, Prize

admin.site.register(Tournament)
admin.site.register(TournamentEntry)
admin.site.register(Prize)

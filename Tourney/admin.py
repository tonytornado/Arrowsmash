from django.contrib import admin

from Tourney.models import Tournament, TournamentEntry, TournamentResult

admin.site.register(Tournament)
admin.site.register(TournamentEntry)
admin.site.register(TournamentResult)

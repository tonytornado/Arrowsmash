from django.contrib import admin

from League.models import League, LeagueEntry, LeagueResult, Trial, TrialEntry

admin.site.register(League)
admin.site.register(LeagueEntry)
admin.site.register(LeagueResult)
admin.site.register(Trial)
admin.site.register(TrialEntry)

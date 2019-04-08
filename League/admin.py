from django.contrib import admin

from League.models import League, LeagueEntry, LeagueResult

admin.site.register(League)
admin.site.register(LeagueEntry)
admin.site.register(LeagueResult)

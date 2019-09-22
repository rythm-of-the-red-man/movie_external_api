from django.contrib import admin

from . models import Movie,ImdbInfo,Rating,Staff,Timeline,MarketingInfo,Comment

admin.site.register(Movie)
admin.site.register(ImdbInfo)
admin.site.register(Rating)
admin.site.register(Staff)
admin.site.register(Timeline)
admin.site.register(MarketingInfo)
admin.site.register(Comment)

from django.contrib import admin


# Register your models here.
from bailout.models import Bailout, UserProfile, Rating

admin.site.register(Bailout)
admin.site.register(UserProfile)
admin.site.register(Rating)
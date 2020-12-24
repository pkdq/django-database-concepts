from django.contrib import admin

from .models import Simple, Movie, Character, Actor

# Register your models here.
admin.site.register(Simple)
admin.site.register(Movie)
admin.site.register(Character)
admin.site.register(Actor)
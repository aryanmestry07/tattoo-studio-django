from django.contrib import admin
from .models import Artist, Category, Tattoo, Booking, Review

admin.site.register(Artist)
admin.site.register(Category)
admin.site.register(Tattoo)
admin.site.register(Booking)
admin.site.register(Review)
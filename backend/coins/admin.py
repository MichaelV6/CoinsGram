from django.contrib import admin
from .models import Coin

@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'estimated_value', 'pub_date')
    list_filter = ('tags', 'pub_date', 'author')
    search_fields = ('name', 'description')
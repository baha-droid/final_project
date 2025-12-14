from django.contrib import admin

from django.contrib import admin
from .models import Brand, CarModel, Car

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand']
    list_filter = ['brand']

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['model', 'year', 'price', 'car_type']
    list_filter = ['car_type', 'model__brand']
    search_fields = ['model__name', 'model__brand__name']


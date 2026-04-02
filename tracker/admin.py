from django.contrib import admin
from .models import Profile, WeightEntry, FoodItem, MealEntry

admin.site.register(Profile)
admin.site.register(WeightEntry)
admin.site.register(FoodItem)
admin.site.register(MealEntry)

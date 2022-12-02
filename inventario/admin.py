from django.contrib import admin

# Register your models here.
from .models import Ingredient
from .models import MenuItem
from .models import Purchase
from .models import RecipeRequirement

admin.site.register(Ingredient)
admin.site.register(MenuItem)
admin.site.register(Purchase)
admin.site.register(RecipeRequirement)


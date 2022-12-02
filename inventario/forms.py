from django import forms
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement

from django.contrib.auth.forms import AuthenticationForm, UsernameField


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = "__all__"
        
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = "__all__"
        
class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = "__all__"
        
class RecipeRequirementForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = "__all__"


class IngredientUpdateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "availableQuantity"]
        
        def __init__(self, *args, **kwargs):
            super(IngredientUpdateForm, self).__init__(*args, **kwargs)
            for field in self.disabled_fields:
                self.fields[field].disabled = True
            
        

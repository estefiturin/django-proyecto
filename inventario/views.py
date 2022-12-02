from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.views.generic import CreateView, DeleteView, UpdateView

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from decimal import *

from .models import MenuItem, Ingredient, Purchase, RecipeRequirement

from .forms import IngredientForm, MenuItemForm, RecipeRequirementForm, PurchaseForm, IngredientUpdateForm
#=============================HOME===================================
class Home():
    pass


#=============================VISTAS===================================
#ver todos los ingredientes en el inventario
class Inventory(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "inventory.html"
    
#eliminar ingredientes del inventario

#ver los elementos en el menu
class Menu(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = "menu.html"
    
    def get_context_data(self):
        context = super().get_context_data() 
        context["recreqs"] = RecipeRequirement.objects.all()
        context["menuitems"] = MenuItem.objects.all()
        context["ingredients"] = Ingredient.objects.all()
        #context["pricesum"] = self.sum_recipe_price()
        return context
    

#ver las compras realizadas en el restaurante
class Purchases(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "purchases.html"
    
    def get_context_data(self):
        context = super().get_context_data()
        context["purchases"] = Purchase.objects.all()
        return context
    

#ver las ganancias y los ingresos del restaurante
class BalanceSheet(LoginRequiredMixin, TemplateView):
    template_name = "balancesheet.html"
    
    @property #calcular el costo total de todos los ingredientes de todos los items
    def total_purchases_cost(self):
        total_cost = Decimal(0.00)
        all_PO = Purchase.objects.all()
        for this_PO in all_PO:
            total_cost += this_PO.menuItem.sum_recipe_prices()
        return total_cost
    
    @property # calcular el precio total de todos los items usados en el menu
    def total_sales_price(self):
        total_price = Decimal(0.00)
        all_PO = Purchase.objects.all()	
        for this_PO in all_PO:
            total_price += this_PO.menuItem.price
        return total_price
    
    def get_context_data(self):
        context = super().get_context_data()
        context["totalcost"] = self.total_purchases_cost
        context["totalsales"] = self.total_sales_price
        context["profitorloss"] = self.total_sales_price - self.total_purchases_cost
        return context

#===========================Logout======================================================
class SignUp(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy("login")
  template_name = "registration/signup.html"
  
def logout_view(request):
  logout(request)
  return redirect("login")


#================CLASES PARA AÑADIR O ACTUALIZAR ITEMS, BASADOS EN FORM=================

class CreateMenuItem(LoginRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "add_menu_item.html"

class CreateIngredient(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = "add_ingredient.html"
    form_class = IngredientForm
    
class UpdateIngredient(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = "update_ingredient.html"
    form_class = IngredientUpdateForm
    
class CreateRecipe(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    template_name = "create_recipe.html"
    form_class = RecipeRequirementForm
    
class CreatePurchase(LoginRequiredMixin, CreateView):
    model = Purchase
    template_name = "create_purchase.html"
    form_class = PurchaseForm 
    
class confirmPurchase(LoginRequiredMixin, ListView):
    template_name = ""
    model = Purchase
    
    def get_context_data(self):
        context = super().get_context_data()
        context["purchase"] = Purchase.objects.get(id=self.kwargs["pk"])
        context["depleteinventory"] = self.deplete
        return context 
    
    @property 
    def deplete_inventory(self):
        thisPI = Purchase.objects.get(id=self.kwargs["pk"])
        rrSet = thisPI.menuItem.reciperequirement_set.all()
        for thisRR in rrSet:
            thisINname = thisRR.ingredient.name
            thisQTY = thisRR.quantity
            ING_TAR = Ingredient.objects.get(name=thisINname)
            ING_TAR.availableQuantity -= thisQTY
            ING_TAR.save()
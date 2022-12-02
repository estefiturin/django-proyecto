from django.db import models
from decimal import *

'''
Modelo Ingredientes: Un inventario con diferentes Ingredientes. Su cantidad disponible y cantidad por unidad
'''
class Ingredient(models.Model):
    OUNCE = 'oz'
    POUND = 'lb'
    UNIT_CHOICES = [
        (OUNCE, 'ounce'),
        (POUND, 'pound'),
    ]
    name = models.CharField(max_length=20)
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES, default='oz')
    availableQuantity = models.IntegerField(default=10)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    
    def get_absolute_url(self):
        return "/inventario"
    def __str__(self):
        return self.name
    

'''
Modelo, una lista de los restaurantes y precio establecido para cada entrada
'''
class MenuItem(models.Model):
    title = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=11.50)
    
    def sum_recipe_prices(self): #total del costo de ingredientes para cada menu
        theTotalPrice = Decimal(0.00)
        theListOfIngredients = self.reciperequirement_set.all()
        for ing in theListOfIngredients:
            theTotalPrice += ing.ingredient_cost
        return theTotalPrice
        
    def get_absolute_url(self):
        return "/menu"
    def __str__(self):
        return f"{self.title}"
    


'''
Una lista de los ingredientes que cada elemento del menu requiere

'''

class Purchase(models.Model):
    date = models.DateField(auto_now=True)
    menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    
    def get_absolute_url(self):
        return f"/purchase/{self.id}/confirm"
    def __str__(self):
        return f"{self.id} {self.menuItem} {self.date}"
    
    
'''
Un registro de todos los hechos en el restaurantes
'''

class RecipeRequirement(models.Model):
    menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=3, decimal_places=0, default=1)
    
    @property #calcular costo de ingredientes usados 
    def ingredient_cost(self):
        return self.ingredient.unitPrice * self.quantity
    
    def get_absolute_url(self):
        return "/menu"
    
    def __str__(self):
        return f"{self.id} {self.menuItem} {self.ingredient} {self.quantity} {self.ingredient_cost}"
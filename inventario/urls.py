from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('balancesheet', views.BalanceSheet.as_view(), name='balancesheet'),
    path('menu', views.Menu.as_view(), name='menu'),
    path('inventory', views.Inventory.as_view(), name='inventory'),
    path('purchases', views.Purchases.as_view(), name='purchases'),
    path("accounts/", include("django.contrib.auth.urls"), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html')),
    #===================================================================
    path("add_menu_item", views.CreateMenuItem.as_view(), name='add_menu_item'),
    path("add_ingredient", views.CreateIngredient.as_view(), name='add_ingredient'),
    path("create_recipe", views.CreateRecipe.as_view(), name='create_recipe'),
    path("create_purchase", views.CreatePurchase.as_view(), name='create_purchase'),
    path("inventory/<pk>/update/", views.UpdateIngredient.as_view(), name='update_ingredient'),
    path("purchase/<pk>/confirm", views.confirmPurchase.as_view(), name='confirm_purchase'),
    
]

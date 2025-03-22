from django.contrib import admin
from .models import Category, RegularPizza, SicilianPizza, Toppings, Sub, Pasta, Salad, DinnerPlatters, UserOrder, SavedCarts
from .widgets import orders
from django.db import models



class CategoryAdmin(admin.ModelAdmin):
    formfield_overrides = {
            models.TextField: {'widget': orders},
            }

class RegularPizzaAdmin(admin.ModelAdmin):
    formfield_overrides = {
            models.TextField: {'widget': orders},
            }

class SicilianPizzaAdmin(admin.ModelAdmin):
    formfield_overrides = {
            models.TextField: {'widget': orders},
            }


admin.site.register(Category,CategoryAdmin)
admin.site.register(RegularPizza, RegularPizzaAdmin)
admin.site.register(SicilianPizza, SicilianPizzaAdmin)
admin.site.register(Toppings)
admin.site.register(Sub)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(DinnerPlatters)
admin.site.register(UserOrder)
admin.site.register(SavedCarts)

from django.contrib import admin
from .models import Pizza, Customer, Order, OrderPizzaRel, PizzaImage, PizzaSize, PizzaSizeRel


class OrderPizzaRelInline(admin.TabularInline):
    model = OrderPizzaRel
    extra = 2


class PizzaImageInline(admin.StackedInline):
    model = PizzaImage


class PizzaSizeInline(admin.TabularInline):
    model = PizzaSizeRel
    extra = 3


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderPizzaRelInline]


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    inlines = [PizzaImageInline, PizzaSizeInline]


admin.site.register(Customer)
admin.site.register(PizzaSize)

from django.contrib import admin
from .models import Customer, Product, Order, CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'in_stock', 'created_at')
    search_fields = ('title', 'category')
    list_filter = ('category', 'in_stock')
    ordering = ('-created_at',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'created_at')
    search_fields = ('username', 'email')
    ordering = ('-created_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_title', 'customer_name', 'customer_email', 'customer_phone', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('customer_name', 'customer_email', 'customer_phone', 'product_title')
    ordering = ('-created_at',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'product_title', 'quantity', 'added_at')
    search_fields = ('user_email', 'product_title')
    ordering = ('-added_at',)
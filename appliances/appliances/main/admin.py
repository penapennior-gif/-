from django.contrib import admin
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available', 'featured', 'featured_order', 'created']
    list_filter = ['available', 'featured', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'available', 'featured', 'featured_order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    raw_id_fields = ['category']
    ordering = ['-created']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'status', 'created']
    list_filter = ['status', 'created', 'updated']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    raw_id_fields = ['user']
    readonly_fields = ['created', 'updated', 'total_price']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity']
    raw_id_fields = ['order', 'product']
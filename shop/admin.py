from django.contrib import admin

from shop.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', 'slug', 'stock_qty', 'price', 'created_at', 'updated_at', 'is_active']
    list_filter = ['vendor', 'created_at',]
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ['vendor']
    date_hierarchy = 'created_at'
    ordering = ['vendor', 'created_at']
    show_facets = admin.ShowFacets.ALWAYS

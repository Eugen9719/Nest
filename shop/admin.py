from django.contrib import admin

from shop.models import Product, Category, ProductMedia, ProductReview


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', 'slug', 'stock_qty', 'price', 'created_at', 'updated_at', 'is_active']
    list_filter = ['vendor', 'created_at', ]
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ['vendor']
    date_hierarchy = 'created_at'
    ordering = ['vendor', 'created_at']
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    ordering = ['name']
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(ProductMedia)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'alt']


admin.site.register(ProductReview)

from django.contrib import admin
from .models import Product, Listing, Tag, Customer

# Register your models here.
# admin.site.register(Product)
# admin.site.register(Listing)
admin.site.register(Tag)
# admin.site.register(Customer)


class TagItemInline(admin.TabularInline):
    model = Tag
    autocomplete_fields = ['listing']
    extra = 0
    min_num = 1
    max_num = 10


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    search_fields = ['name']
    prepopulated_fields = {
        'slug': ['name']
    }
    inlines = [TagItemInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['customer', 'listing', 'payment_status', 'lease_date', 'clear_date']
    list_editable = ['payment_status']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
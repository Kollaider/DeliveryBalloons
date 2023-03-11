from django.contrib import admin

from webapp.models import Product, ProductImage, Category, UserPayment

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Category)

@admin.register(UserPayment)
class UserRegister(admin.ModelAdmin):
    list_display = ['pk', 'product', 'quantity', 'is_paid', 'is_delivered']

from django.contrib import admin

from webapp.models import Product,  UserPayment, Banner, Content

admin.site.register(Product)
# admin.site.register(ProductImage)
# admin.site.register(Category)

@admin.register(UserPayment)
class UserPaymentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'product', 'quantity', 'is_paid', 'is_delivered']
    list_filter = ['is_paid', 'is_delivered', 'quantity']
    search_fields = ['email', 'address', 'stripe_checkout_id', 'comment']
    list_editable = ['is_delivered',]



@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['name']

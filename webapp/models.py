from django.contrib.auth.models import User
from django.db import models
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class CreateTimeMixin(models.Model):
    """Mixin for adding create_at field into model"""

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdateTimeMixin(models.Model):
    """Mixin for adding updated_at field into model"""

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(CreateTimeMixin, UpdateTimeMixin, models.Model):
    """Product Model"""

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """Product Images Model"""
    products = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')


class Category(models.Model):
    """Category Model"""
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class UserPayment(models.Model):
    stripe_checkout_id = models.CharField(max_length=500)
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    email = models.EmailField(null=True, blank=True)
    comment = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField()
    delivery_time = models.DateTimeField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_payment(sender, instance, created, **kwargs):
    if created:
        UserPayment.objects.create(app_user=instance)



class Banner(models.Model):
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to='banner', help_text='Image resolution should be 1920x896 pixels')



class Content(models.Model):
    name = models.CharField(max_length=300, help_text='Image resolution should be 600х600 pixels')
    text = models.TextField()

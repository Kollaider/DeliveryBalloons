from django.db import models

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
    price = models.PositiveIntegerField()
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
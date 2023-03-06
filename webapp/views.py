from django.shortcuts import render
from django.views.generic import DetailView, TemplateView

from webapp.models import Product



class HomePage(TemplateView):
    template_name = 'webapp/index.html'

    def get_context_data(self, **kwargs):
        products = Product.objects.all()
        context = {}
        context['products'] = products
        return super().get_context_data(**context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'webapp/product-details.html'


class AboutView(TemplateView):
    template_name = 'webapp/about-us.html'


class ContactView(TemplateView):
    template_name = 'webapp/contact-us.html'

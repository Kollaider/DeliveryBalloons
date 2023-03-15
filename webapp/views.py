from datetime import datetime
from itertools import zip_longest

from django.views.generic import DetailView, TemplateView

from webapp.models import Product, Content, Banner
from webapp.utils import get_times_intervals
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from webapp.models import UserPayment
import stripe
import time
from django.shortcuts import render, redirect


class HomePage(TemplateView):
    template_name = 'webapp/index.html'

    def get_context_data(self, **kwargs):
        context = {}
        products = Product.objects.all()
        lst1, lst2 = [p1 for p1 in products[::2]], [p2 for p2 in products[1::2]]
        context['products'] = zip_longest(lst1, lst2)
        content_about_us = Content.objects.get(name='about_us').text
        context['content_about_us'] = content_about_us
        context['banners'] = Banner.objects.all()
        return super().get_context_data(**context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'webapp/product_detail.html'


class AboutView(TemplateView):
    template_name = 'webapp/about-us.html'


class ContactView(TemplateView):
    template_name = 'webapp/contact-us.html'


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}

    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(product.price * 100),
                        'product_data': {
                            'name': product.name,
                        },
                    },
                    'quantity': quantity,
                },
            ],
            mode='payment',
            customer_creation='always',
            success_url=settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled',

            shipping_address_collection={
                "allowed_countries": ["US"],
            },
            allow_promotion_codes=True,
            billing_address_collection="required",
            phone_number_collection={
                'enabled': True,
            },

            payment_intent_data={
                'metadata': {
                    'delivery_options': 'dropdown',
                    'delivery_options_values': 'Option 1,Option 2,Option 3',
                }
            },
            custom_fields=[
                {
                    "key": "comment",
                    "label": {"type": "custom", "custom": "Comment"},
                    "type": "text",
                },
                {
                    "key": "deliverytime",
                    "label": {"type": "custom", "custom": "Delivery time"},
                    "optional": False,
                    "type": "dropdown",
                    "dropdown": {
                        "options": get_times_intervals()
                    },
                },
            ],
            metadata={
                "product_id": pk,
                "quantity": quantity
            }
        )
        UserPayment.objects.create(
            stripe_checkout_id=checkout_session.stripe_id,
            product_id=pk,
            quantity=quantity
        )
        return redirect(checkout_session.url, code=303)

    return render(request, 'webapp/product_detail.html', context=context)


def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)

    user_payment = UserPayment.objects.get(stripe_checkout_id=checkout_session_id)
    user_payment.is_paid = True
    user_payment.email = session.customer_details.email
    user_payment.phone = session.customer_details.phone
    user_payment.comment = session.custom_fields[0].text['value']
    user_payment.delivery_time = datetime.strptime(session.custom_fields[1].dropdown['value'], '%Y%m%dT%H%M%S')
    address = session.shipping_details.address
    user_payment.address = f'{address.line1}, {address.line2}, {address.city}, {address.postal_code}'
    user_payment.quantity = int(session.metadata.quantity)
    user_payment.save()

    return render(request, 'webapp/payment_successful.html', {'customer': customer})


def payment_cancelled(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    return render(request, 'webapp/payment_cancelled.html')


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        user_payment.payment_bool = True
        user_payment.save()
    return HttpResponse(status=200)


from django.urls import reverse_lazy, reverse
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
    template_name = 'webapp/product_detail.html'


class AboutView(TemplateView):
    template_name = 'webapp/about-us.html'


class ContactView(TemplateView):
    template_name = 'webapp/contact-us.html'


from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from webapp.models import UserPayment
import stripe
import time


# @login_required(login_url='login')
def product_detail(request, pk):

    product = Product.objects.get(pk=pk)
    context = {'product': product}

    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': settings.PRODUCT_PRICE,
                    'quantity': int(request.POST.get('quantity')),
                },
            ],
            mode='payment',
            customer_creation='always',
            success_url=settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled',
            # shipping_rates=[
            #     "your_shipping_rate_id",
            # ],
            shipping_address_collection={
                "allowed_countries": ["US"],
            },
            allow_promotion_codes=True,
            billing_address_collection="required",

            # locale="auto",
            # submit_type="pay",
            custom_fields=[
                {
                    "key": "comment",
                    "label": {"type": "custom", "custom": "Personalized engraving"},
                    "type": "text",
                },
            ],

        )
        return redirect(checkout_session.url, code=303)

    return render(request, 'webapp/product_detail.html', context=context)



## use Stripe dummy card: 4242 4242 4242 4242
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    # user_id = request.user.user_id
    # user_id = 1
    # user_payment = UserPayment.objects.get(app_user=user_id)
    # user_payment.stripe_checkout_id = checkout_session_id
    # user_payment.save()
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


from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages


def home(request):
    return render(request, 'general/home.html')


def user_signup(request):
    if request.method == 'POST':
        user_email = request.POST['user_email']
        username = request.POST['username']
        user_pswd = request.POST['user_pass']
        user_model = get_user_model()
        ##
        if not username.strip():
            messages.error(request, 'Something is wrong.')
            return render(request, 'app_users/signup.html')
        ##
        if user_model.objects.filter(email=user_email).exists():
            messages.error(request, 'Something is wrong.')
            return render(request, 'app_users/signup.html')
        ##
        user_obj = user_model.objects.create_user(email=user_email, password=user_pswd)
        user_obj.set_password(user_pswd)
        user_obj.username = username
        user_obj.save()
        user_auth = authenticate(username=user_email, password=user_pswd)
        ##
        if user_auth:
            login(request, user_auth)
            return redirect('home')
    return render(request, 'app_users/signup.html')


def user_login(request):
    if request.method == 'POST':
        user_email = request.POST['user_email']
        user_pswd = request.POST['user_pass']
        try:
            user_auth = authenticate(username=user_email, password=user_pswd)
            login(request, user_auth)
            return redirect('home')
        except:
            messages.error(request, 'Something is wrong.')
            return render(request, 'app_users/login.html')
    else:
        return render(request, 'app_users/login.html')


def user_logout(request):
    try:
        logout(request)
    except:
        messages.error(request, 'Something is wrong.')
    return redirect('login')

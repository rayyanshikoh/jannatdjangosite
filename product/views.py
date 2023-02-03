from .models import Customer, Product, Listing
from .forms import availabilityForm, confirmForm, customerForm

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

import stripe
import datetime


# Assistive Functions
def deltadate(start_date, end_date):
    delta_date = (datetime.datetime.strptime(end_date, '%Y-%m-%d')) - (
        datetime.datetime.strptime(start_date, '%Y-%m-%d'))
    print(delta_date.days)
    return int(delta_date.days)


# Base views
def homepage(request):
    if request.method == 'POST':
        start_date = datetime.datetime.strptime(request.POST.get("start_date"), '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(request.POST.get("end_date"), '%Y-%m-%d').date()
        return redirect('datesearch', start_date=start_date, end_date=end_date)
    else:
        return render(request, 'website/index.html')


def aboutus(request):
    return render(request, 'website/about.html')


def search_products(request, start_date, end_date):
    print(f"Start Date: {start_date}, End Date: {end_date}")
    print(
        f"Excluding products that are gonna clear out after {start_date} and that are gonna be leased before {end_date}")
    filtered_list = Listing.objects.exclude(product__clear_date__gt=start_date, product__lease_date__lt=end_date)
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'listing': filtered_list
    }
    return render(request, 'website/products.html', context=context)


def search_listing(request, start_date, end_date, product_name):
    listing = Listing.objects.get(slug=product_name)
    listing.short_term_price = listing.short_term_price / 100
    listing.long_term_price = listing.long_term_price / 100
    if request.method == 'POST':
        form = availabilityForm(request.POST)
        if form.is_valid():
            lease_date = form.cleaned_data['start_date']
            clear_date = form.cleaned_data['end_date']
            # Here, enter validation to ensure that the listing is available
            return redirect(customerform, product_name=listing.slug, lease_date=lease_date, clear_date=clear_date)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = availabilityForm()
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'listing': [listing],
        'form': form
    }
    return render(request, 'website/listing.html', context=context)


def products(request):
    listings = Listing.objects.all()
    context = {
        'listing': listings
    }
    return render(request, 'website/products.html', context=context)


def listing(request, product_name):
    listing = Listing.objects.get(slug=product_name)
    listing.short_term_price = listing.short_term_price / 100
    listing.long_term_price = listing.long_term_price / 100
    if request.method == 'POST':
        form = availabilityForm(request.POST)
        if form.is_valid():
            lease_date = form.cleaned_data['start_date']
            clear_date = form.cleaned_data['end_date']
            # Here, enter validation to ensure that the listing is available
            return redirect(customerform, product_name=listing.slug, lease_date=lease_date, clear_date=clear_date)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = availabilityForm()
    context = {
        'listing': [listing],
        'form': form
    }
    return render(request, 'website/listing.html', context=context)


def customerform(request, product_name, lease_date, clear_date):
    listing = Listing.objects.get(slug=product_name)
    delta_date = deltadate(start_date=lease_date, end_date=clear_date)
    if delta_date > 31:
        price = delta_date * listing.long_term_price
    else:
        price = delta_date * listing.short_term_price
    if request.method == 'POST':
        form = customerForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            date_of_birth = form.cleaned_data['date_of_birth']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            customer = Customer.objects.update_or_create(first_name=first_name, last_name=last_name,
                                                      dateofbirth=date_of_birth, email=email, phone_number=phone_number)
            return redirect(confirm, product_name=listing.slug, lease_date=lease_date, clear_date=clear_date,
                            customer=email, price=price)
    else:
        form = customerForm()
    context = {
        'listing': [listing],
        'form': form,
        'price': price
    }
    return render(request, 'website/customerform.html', context=context)


def confirm(request, product_name, lease_date, clear_date, customer, price):
    listing = Listing.objects.get(slug=product_name)
    customer = Customer.objects.get(email=customer)
    delta_date = deltadate(start_date=lease_date, end_date=clear_date)
    product = Product.objects.create(
        listing=listing,
        customer=customer,
        lease_date=lease_date,
        clear_date=clear_date,
        price=price
    )
    form = confirmForm(request.POST)
    if form.is_valid():
        print("Order confirmed, redirecting")
        return redirect('landing-page', pk=product.pk)
    if delta_date > 31:
        price = delta_date * listing.long_term_price
    else:
        price = delta_date * listing.short_term_price
    context = {
        'listing': [listing],
        'lease_date': lease_date,
        'clear_date': clear_date,
        'first_name': customer.first_name,
        'last_name': customer.last_name,
        'date_of_birth': customer.dateofbirth,
        'email': customer.email,
        'phone_number': customer.phone_number,
        'price': price
    }
    return render(request, 'website/confirmation.html', context=context)


def store(request):
    return render(request, 'website/store.html')


# Stripe Views
public_key = settings.STRIPE_PUBLIC_KEY
secret_key = settings.STRIPE_SECRET_KEY

stripe.api_key = secret_key


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'


class ProductLandingPageView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": public_key
        })
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            # line_items=[
            #     {
            #         # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
            #         'price': '{{PRICE_ID}}',
            #         'quantity': 1,
            #     },
            # ],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.listing.name,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png']
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product_id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        # Fulfill the purchase...
        # fulfill_order(session)
    # Passed signature verification
    return HttpResponse(status=200)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print('Checkout completed, sending email')
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["product_id"]
        product = Product.objects.get(id=product_id)
        product.payment_status = 'C'
        product.save()
        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase.",
            recipient_list=[customer_email],
            from_email=settings.EMAIL_HOST_USER
        )
    return HttpResponse(status=200)

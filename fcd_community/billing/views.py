import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse

from fcd_community.billing.tasks import validate_user_credit_cards


# Create your views here.
@login_required
def billing_home(request: HttpRequest):
    return render(request, 'billing/billing_home.html')


@login_required
def checkout_session(request: HttpRequest):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if request.user.stripe_customer_id:
            customer_id = request.user.stripe_customer_id
        else:
            customer = stripe.Customer.create(
                email=request.user.email,
            )
            customer_id = customer['id']
            request.user.stripe_customer_id = customer_id
            request.user.save()
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='setup',
            customer=customer_id,
            success_url=request.build_absolute_uri(
                reverse('billing:checkout_success')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://example.com/cancel',
        )

        return redirect(session.url, code=303)
    return render(request, 'billing/checkout_session.html')


@login_required
def checkout_success(request: HttpRequest):
    session_id = request.GET['session_id']
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    print(session)

    return render(request, 'billing/checkout_success.html')

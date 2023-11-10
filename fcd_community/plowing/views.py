from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect

from fcd_community.plowing.models import PlowingService, PlowingRequest


# Create your views here.
def plowing_home(request: HttpRequest):
    avail_services = PlowingService.objects.exclude(provider=request.user)
    avail_requests = PlowingRequest.objects.filter(service__provider=request.user, status='pending')
    return render(request, 'plowing/plowing_home.html',
                  {'avail_services': avail_services, 'avail_requests': avail_requests})


def plowing_service(request: HttpRequest, service_id: str):
    service: PlowingService = get_object_or_404(PlowingService, pk=service_id)
    PlowingRequest.objects.create(service=service, requestor=request.user)

    messages.add_message(request, messages.SUCCESS, 'Your request has been sent to the service provider.')
    return redirect('plowing:home')


def manage_request(request: HttpRequest, request_id:str):
    p_req: PlowingRequest = get_object_or_404(PlowingRequest, pk=request_id)
    action = request.GET['action']
    if action == 'accept':
        if p_req.charge_customer():
            messages.add_message(request, messages.SUCCESS, 'Payment successful. You may now plow.')
        else:
            messages.add_message(request, messages.ERROR, 'Payment failed. Please try again.')
    elif action == 'reject':
        p_req.status = 'rejected'
        p_req.save()

    return redirect('plowing:home')


import stripe
from django.conf import settings
from django.db import models

from fcd_community.utils.models import BaseModel


# Create your models here.
class PlowingService(BaseModel):
    provider = models.ForeignKey('users.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='Plowing Service')
    price = models.DecimalField(max_digits=10, decimal_places=2)


class PlowingRequest(BaseModel):
    service = models.ForeignKey('plowing.PlowingService', on_delete=models.CASCADE)
    requestor = models.ForeignKey('users.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'),
                                       ('completed', 'Completed')], default='pending')

    def charge_customer(self) -> bool:

        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY



            invoice = stripe.Invoice.create(
                customer=self.requestor.stripe_customer_id,
                auto_advance=True,
                collection_method='charge_automatically',
                currency='eur'
            )


            stripe.InvoiceItem.create(
                customer=self.requestor.stripe_customer_id,
                amount=int(self.service.price * 100),
                description=self.service.name,
                currency='eur',
                invoice=invoice.id
            )
            self.status = 'completed'
            self.save()
            return True
        except Exception as e:
            return False

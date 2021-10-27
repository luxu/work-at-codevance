from rest_framework import serializers

from payments.models import Payments


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = (
            "id",
            "provider",
            "issue_date",
            "due_date",
            "advance_date",
            "original_value",
            "decision",
            "discount_value",
            "value_new",
        )


class PaymentsListFilterSerializer(serializers.ModelSerializer):

    def __init__(self, payment_id=None, list=None, token=None):
        self.payment_id = payment_id
        self.payments = list
        self.token = token

    @property
    def data(self):
        if self.payment_id is not None:
            payment = Payments.objects.filter(id=self.payment_id)
            return self.list_payments(self.payment_id)
        return self.list_payments(self.payment_id)

    def list_payments(self, payment_id):
        return Payments.objects.get(id=payment_id)

    class Meta:
        model = Payments
        fields = (
            "id",
            "provider",
            "issue_date",
            "due_date",
            "advance_date",
            "original_value",
            "decision",
            "discount_value",
            "value_new",
        )

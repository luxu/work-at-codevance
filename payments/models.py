from django.db import models

from providers.models import Providers


class Payments(models.Model):
    SEM_PEDIDO = 0
    APROVADOS = 1
    NEGADOS = 2
    AGUARDANDO_LIBERACAO = 3

    DECISION_STATUS = (
        (0, "Sem pedido"),
        (1, "Aprovado"),
        (2, "Negado"),
        (3, "Aguardando liberação"),
    )

    provider = models.ForeignKey(
        Providers,
        on_delete=models.CASCADE
    )
    issue_date = models.DateField(
        'Data da emissão',
        null=True,
        blank=True
    )
    due_date = models.DateField(
        'Data do vencimento',
        null=True,
    )
    advance_date = models.DateField(
        'Data Antecipação',
        null=True,
        blank=True
    )
    original_value = models.DecimalField(
        'Valor Original',
        max_digits=6,
        decimal_places=2,
    )
    decision = models.IntegerField(
        'Decisão',
        default=0,
        choices=DECISION_STATUS
    )
    discount_value = models.DecimalField(
        'Valor com Desconto',
        max_digits=6,
        decimal_places=2,
        default=0
    )
    value_new = models.DecimalField(
        'Valor Final',
        max_digits=6,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.provider.corporate_name

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'


class PaymentsLogs(models.Model):
    provider = models.ForeignKey(
        Providers,
        on_delete=models.CASCADE
    )
    issue_date = models.DateField(
        'Data da emissão',
        null=True,
    )
    due_date = models.DateField(
        'Data do vencimento',
        null=True,
    )
    original_value = models.DecimalField(
        'Valor Original',
        max_digits=6,
        decimal_places=2,
    )
    anticipated_amount = models.BooleanField(
        'Valor antecipado',
        default=False,
        # choices=
    )

    def __str__(self):
        return self.provider.corporate_name

    class Meta:
        verbose_name = 'Log Pagamento'
        verbose_name_plural = 'Logs Pagamentos'

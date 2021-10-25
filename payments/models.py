from django.db import models

from providers.models import Providers


class Payments(models.Model):
    provider = models.ForeignKey(
        Providers,
        on_delete=models.CASCADE
    )
    issue_date = models.DateField(
        'Data da emissão',
        null=True,
    )
    due_date = models.DateField(
        'Data do vencimentp',
        null=True,
    )
    original_value = models.DecimalField(
        'Valor Original',
        max_digits=6,
        decimal_places=2,
    )

    def __str__(self):
        return self.provider.corporate_name

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

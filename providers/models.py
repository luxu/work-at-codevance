from django.db import models


class Providers(models.Model):
    cnpj = models.CharField(
        max_length=14,
    )
    corporate_name = models.CharField(
        'Razão Social',
        max_length=30,
        blank=True
    )

    def __str__(self):
        return self.corporate_name

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'


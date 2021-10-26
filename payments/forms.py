from django import forms

from .models import Payments


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class PaymentsForm(forms.ModelForm):
    class Meta:
        model = Payments
        exclude = [
            'issue_date',
            'advance_date',
            'decision',
            'discount_value',
            'value_new',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['original_value'].localize = True
        self.fields['original_value'].widget.is_localized = True
        self.fields["due_date"].widget = DateInput()

    widgets = {
        'original_value': forms.DecimalField(decimal_places=2, max_digits=5),
    }

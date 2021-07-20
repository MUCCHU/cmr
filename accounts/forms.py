from django.db.models import fields
from django.forms import ModelForm
from .models import order

class orderForm(ModelForm):
    class Meta:
        model= order
        fields = "__all__"
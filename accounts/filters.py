from django.db.models import fields
import django_filters
from .models import *
class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = order
        fields = '__all__'
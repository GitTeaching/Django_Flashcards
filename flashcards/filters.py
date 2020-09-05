import django_filters
from .models import FlashCard
from django_filters import DateFilter


class OrderFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name="date_created", lookup_expr="gte")
	class Meta:
		model = FlashCard
		fields = ['front', 'back', 'category']
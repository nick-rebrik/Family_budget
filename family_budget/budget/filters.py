import django_filters as filters

from .models import BudgetOperation


class OperationFilter(filters.FilterSet):
    category = filters.CharFilter(
        field_name='category__title',
        lookup_expr='contains'
    )

    class Meta:
        model = BudgetOperation
        fields = ('category', 'operation_type')

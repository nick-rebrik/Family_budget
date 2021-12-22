import django_filters as filters

from .models import BudgetOperation


class OperationFilter(filters.FilterSet):
    title = filters.CharFilter(
        field_name='category__title',
        lookup_expr='contains'
    )

    class Meta:
        model = BudgetOperation
        fields = ('title', 'operation_type')

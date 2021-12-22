from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (BudgetsListViewSet, BudgetViewSet, CategoryViewSet,
                    BudgetOperationViewSet, ShareViewSet)

app_name = 'budget'

router_v1 = DefaultRouter()
router_v1.register('lists', BudgetsListViewSet, basename='Budgets_lists')
router_v1.register(
    'lists/(?P<list_id>[0-9]+)/budgets',
    BudgetViewSet,
    basename='Budgets'
)
router_v1.register('categories', CategoryViewSet, basename='Categories')
router_v1.register(
    ('lists/(?P<list_id>[0-9]+)/budgets/(?P<budget_id>[0-9]+)/'
     'operation'),
    BudgetOperationViewSet,
    basename='Budget_operation'
)
router_v1.register(
    'lists/(?P<list_id>[0-9]+)/share',
    ShareViewSet,
    basename='Share_list'
)

urlpatterns = [
    path('', include(router_v1.urls)),
]
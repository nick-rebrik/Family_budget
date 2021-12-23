from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (BudgetOperationViewSet, BudgetViewSet, BudgetsListViewSet,
                    CategoryViewSet, ShareViewSet)

app_name = 'budget'

router_v1 = DefaultRouter()
router_v1.register('lists', BudgetsListViewSet, basename='budgets_lists')
router_v1.register(
    'lists/(?P<list_id>[0-9]+)/budgets',
    BudgetViewSet,
    basename='budgets'
)
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register(
    ('lists/(?P<list_id>[0-9]+)/budgets/(?P<budget_id>[0-9]+)/'
     'operation'),
    BudgetOperationViewSet,
    basename='budget_operation'
)
router_v1.register(
    'lists/(?P<list_id>[0-9]+)/share',
    ShareViewSet,
    basename='share_list'
)

urlpatterns = [
    path('', include(router_v1.urls)),
]
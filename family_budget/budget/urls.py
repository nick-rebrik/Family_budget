from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BudgetsListViewSet

app_name = 'budget'

router_v1 = DefaultRouter()
router_v1.register('lists', BudgetsListViewSet, basename='Budgets_lists')

urlpatterns = [
    path('', include(router_v1.urls))
]
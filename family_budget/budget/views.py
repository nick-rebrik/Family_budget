from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .models import BudgetsList, Budget
from .serializers import (BudgetsListSerializer, BudgetSerializer,
                          BudgetCreateSerializer)


class BudgetsListViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetsListSerializer

    def get_queryset(self):
        user = self.request.user
        return user.budgets_lists.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class BudgetViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        budgets_list = get_object_or_404(
            BudgetsList, id=self.kwargs['list_id']
        )
        return budgets_list.budgets.all()

    def perform_create(self, serializer):
        user = self.request.user
        budget_list = get_object_or_404(
            BudgetsList, id=self.kwargs['list_id']
        )
        serializer.save(user=user, budget_list=budget_list)

    def get_serializer_class(self):
        if self.action == 'create':
            return BudgetCreateSerializer
        return BudgetSerializer

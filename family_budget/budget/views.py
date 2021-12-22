from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .models import Budget, BudgetsList, Category
from .serializers import (BudgetCreateSerializer, BudgetOperationSerializer,
                          BudgetSerializer, BudgetsListSerializer,
                          CategorySerializer, ShortBudgetSerializer)


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
        elif self.action == 'list':
            return ShortBudgetSerializer
        return BudgetSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BudgetOperationViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetOperationSerializer

    def get_queryset(self):
        budget = get_object_or_404(Budget, id=self.kwargs['budget_id'])
        return budget.budget_operations.all()

    def perform_create(self, serializer):
        budget = get_object_or_404(Budget, id=self.kwargs['budget_id'])
        serializer.save(budget=budget)
